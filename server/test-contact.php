<?php
declare(strict_types=1);
require __DIR__.'/contact-lib.php';
$dir=sys_get_temp_dir().'/glix-contact-test-'.bin2hex(random_bytes(8));mkdir($dir,0700);
$secret=str_repeat('a',64);file_put_contents($dir.'/secret',$secret);
$calls=0;$send=function($reply,$body)use(&$calls){$calls++;return true;};
function expect(bool $value,string $message):void {if(!$value)throw new RuntimeException($message);}
$now=1700000100;$ip='192.0.2.10';$origin='https://glixerp.com';
$data=['name'=>'Persona de prueba','company'=>'Empresa de prueba','email'=>'persona@example.com','phone'=>'','interest'=>'integral','message'=>'Consulta de validación automatizada.','website'=>'','token'=>glix_token($secret,$ip,$now-3)];
try {
    $call=fn($input,$source='https://glixerp.com')=>glix_process('POST',$source,json_encode($input),$ip,$dir,$send,$now);
    expect($call($data,'https://not-glix.example')[0]===403,'Reject foreign origin');
    $bad=$data;$bad['email']="a@example.com\r\nBcc: other@example.com";expect($call($bad)[0]===422,'Reject header injection');
    $bad=$data;$bad['name']=[];expect($call($bad)[0]===422,'Reject arrays');
    $bad=$data;$bad['website']='bot';expect($call($bad)[0]===422,'Reject honeypot');
    $bad=$data;$bad['token']=glix_token($secret,$ip,$now-8000);expect($call($bad)[0]===422,'Reject expired token');
    $bad=$data;$bad['token']=glix_token($secret,$ip,$now);expect($call($bad)[0]===422,'Reject instant submissions');
    $bad=$data;$bad['token']=glix_token($secret,'192.0.2.11',$now-3);expect($call($bad)[0]===422,'Bind token to IP');
    expect($calls===0,'Invalid requests must not send mail');
    expect($call($data)[0]===200 && $calls===1,'Accept valid request');
    expect($call($data)[0]===200 && $calls===1,'Idempotent retry');
    $changed=$data;$changed['message']='Una consulta diferente con el mismo token.';expect($call($changed)[0]===422,'Reject edited replay');
    for($i=0;$i<4;$i++){$data['token']=glix_token($secret,$ip,$now-3);expect($call($data)[0]===200,'Within rate limit');}
    $data['token']=glix_token($secret,$ip,$now-3);expect($call($data)[0]===429 && $calls===5,'Enforce per-IP limit');
    $failure=glix_process('POST',$origin,json_encode(array_merge($data,['token'=>glix_token($secret,'192.0.2.20',$now-3)])),'192.0.2.20',$dir,fn()=>false,$now);
    expect($failure[0]===503,'Do not show success when transport fails');
    echo "PASS: contact validation, origin, token, replay, spam limits and failed transport; no real email sent.\n";
} finally {foreach(['secret','limits.json']as$name)if(is_file($dir.'/'.$name))unlink($dir.'/'.$name);rmdir($dir);}
