<?php
declare(strict_types=1);

const GLIX_ORIGINS = ['https://glixerp.com', 'https://www.glixerp.com', 'https://mail.glixerp.com'];
const GLIX_TOPICS = ['integral'=>'Gestión integral', 'transporte'=>'Transporte y liquidación', 'proveedores'=>'Compras y proveedores', 'personas'=>'Recursos humanos', 'ventas'=>'Ventas y operación en campo', 'consulta'=>'Otra consulta'];

function glix_token(string $secret, string $ip, int $now): string {
    $payload = $now . '.' . bin2hex(random_bytes(16)) . '.' . hash_hmac('sha256', $ip, $secret);
    return $payload . '.' . hash_hmac('sha256', $payload, $secret);
}
function glix_valid_token(string $token, string $secret, string $ip, int $now): bool {
    if (!preg_match('/^(\d{10})\.([a-f0-9]{32})\.([a-f0-9]{64})\.([a-f0-9]{64})$/D', $token, $parts)) return false;
    $payload = $parts[1].'.'.$parts[2].'.'.$parts[3];
    return $now-(int)$parts[1] >= 2 && $now-(int)$parts[1] <= 7200
        && hash_equals(hash_hmac('sha256', $ip, $secret), $parts[3])
        && hash_equals(hash_hmac('sha256', $payload, $secret), $parts[4]);
}
function glix_fields(array $input): array {
    $limits = ['name'=>160, 'company'=>240, 'email'=>254, 'phone'=>80, 'interest'=>30, 'message'=>8000, 'website'=>200, 'token'=>220];
    $data=[];
    foreach ($limits as $key=>$limit) {
        $value=$input[$key]??'';
        if (!is_string($value) || strlen($value)>$limit || preg_match('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', $value)) throw new InvalidArgumentException('Revisá los datos del formulario.');
        $data[$key]=trim($value);
    }
    foreach (['name','company','email','phone','interest','website','token'] as $key) {
        if (strpbrk($data[$key], "\r\n")!==false) throw new InvalidArgumentException('Revisá los datos del formulario.');
    }
    if (strlen($data['name'])<2 || strlen($data['company'])<2 || strlen($data['message'])<10) throw new InvalidArgumentException('Completá tu nombre, empresa y un mensaje de al menos 10 caracteres.');
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL) || !array_key_exists($data['interest'],GLIX_TOPICS)) throw new InvalidArgumentException('Revisá el email y el área de interés.');
    return $data;
}
function glix_process(string $method, string $origin, string $raw, string $ip, string $directory, callable $send, ?int $time=null): array {
    $now=$time??time();
    if (!in_array($origin, GLIX_ORIGINS, true)) return [403,['ok'=>false,'message'=>'Origen no permitido.']];
    if ($method==='OPTIONS') return [204,[]];
    if (!in_array($method,['GET','POST'],true)) return [405,['ok'=>false,'message'=>'Método no permitido.']];
    $secret=trim((string)file_get_contents($directory.'/secret'));
    if (strlen($secret)<64) throw new RuntimeException('Invalid contact configuration');
    if ($method==='GET') return [200,['token'=>glix_token($secret,$ip,$now)]];
    if (strlen($raw)>16000) return [413,['ok'=>false,'message'=>'El mensaje es demasiado largo.']];
    try {
        $input=json_decode($raw,true,16,JSON_THROW_ON_ERROR);
        if (!is_array($input)) throw new InvalidArgumentException('Formulario inválido.');
        $data=glix_fields($input);
    } catch (JsonException|InvalidArgumentException $error) {
        return [422,['ok'=>false,'message'=>$error instanceof JsonException ? 'Formulario inválido.' : $error->getMessage()]];
    }
    if ($data['website']!=='') return [422,['ok'=>false,'message'=>'No pudimos validar la consulta. Intentá nuevamente.']];
    if (!glix_valid_token($data['token'],$secret,$ip,$now)) return [422,['ok'=>false,'message'=>'La validación venció. Volvé a presionar Enviar consulta.']];
    $handle=fopen($directory.'/limits.json','c+');
    if (!$handle || !flock($handle,LOCK_EX)) throw new RuntimeException('Cannot lock contact state');
    try {
        $rawState=stream_get_contents($handle);
        $state=$rawState!=='' ? json_decode($rawState,true,32,JSON_THROW_ON_ERROR) : ['clients'=>[], 'global'=>[], 'used'=>[]];
        $state['emails']=$state['emails']??[];
        $state['messages']=array_filter($state['messages']??[],fn($t)=>$t>$now-600);
        foreach ($state['emails'] as $key=>$times) {
            $times=array_values(array_filter($times,fn($t)=>$t>$now-3600));
            if ($times) $state['emails'][$key]=$times; else unset($state['emails'][$key]);
        }
        $state['global']=array_values(array_filter($state['global'],fn($t)=>$t>$now-3600));
        $state['used']=array_filter($state['used'],fn($item)=>$item['time']>$now-7200);
        foreach ($state['clients'] as $key=>$times) {
            $times=array_values(array_filter($times,fn($t)=>$t>$now-3600));
            if ($times) $state['clients'][$key]=$times; else unset($state['clients'][$key]);
        }
        $client=hash_hmac('sha256',$ip,$secret);
        $id=hash('sha256',$data['token']);
        $fingerprint=hash('sha256',json_encode(array_diff_key($data,['token'=>true]),JSON_THROW_ON_ERROR));
        if (isset($state['used'][$id])) {
            return hash_equals($state['used'][$id]['fingerprint'],$fingerprint) ? [200,['ok'=>true]] : [422,['ok'=>false,'message'=>'La consulta cambió. Volvé a presionar Enviar consulta.']];
        }
        // Hashes only: limit a sender across IPs and suppress identical re-submissions.
        $email=hash_hmac('sha256',strtolower($data['email']),$secret);
        $message=hash_hmac('sha256',json_encode([strtolower($data['email']),$data['name'],$data['company'],$data['phone'],$data['interest'],$data['message']],JSON_THROW_ON_ERROR),$secret);
        if (isset($state['messages'][$message])) return [200,['ok'=>true]];
        if (count($state['emails'][$email]??[])>=5 || count($state['clients'][$client]??[])>=5 || count($state['global'])>=100) return [429,['ok'=>false,'message'=>'Recibimos varias consultas. Esperá un momento o escribinos a info@glixerp.com.']];
        $state['emails'][$email][]=$now;
        $state['clients'][$client][]=$now;
        $state['global'][]=$now;
        $body="Nueva consulta desde la web de GLIX\n\nNombre: ".$data['name']."\nEmpresa: ".$data['company']."\nEmail: ".$data['email']."\nTeléfono: ".($data['phone']?:'No informado')."\nInterés: ".GLIX_TOPICS[$data['interest']]."\n\nMensaje:\n".$data['message']."\n";
        $accepted=$send($data['email'],$body);
        if ($accepted) {
            $state['used'][$id]=['time'=>$now,'fingerprint'=>$fingerprint];
            $state['messages'][$message]=$now;
        }
        rewind($handle);ftruncate($handle,0);
        if (fwrite($handle,json_encode($state,JSON_THROW_ON_ERROR))===false) throw new RuntimeException('Cannot update contact state');
        fflush($handle);
        return $accepted ? [200,['ok'=>true]] : [503,['ok'=>false,'message'=>'No pudimos enviar la consulta. Intentá nuevamente o escribinos a info@glixerp.com.']];
    } finally {flock($handle,LOCK_UN);fclose($handle);}
}
