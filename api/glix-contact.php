<?php
declare(strict_types=1);
ini_set('display_errors','0');
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, max-age=0');
header('X-Content-Type-Options: nosniff');
header('X-Robots-Tag: noindex, nofollow');
header('Vary: Origin');
$directory=dirname(__DIR__,2).'/.glix-contact';
try {
    require $directory.'/contact-lib.php';
    $origin=$_SERVER['HTTP_ORIGIN']??'';
    if (in_array($origin,GLIX_ORIGINS,true)) {
        header('Access-Control-Allow-Origin: '.$origin);
        header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
        header('Access-Control-Allow-Headers: Content-Type');
        header('Access-Control-Max-Age: 600');
    }
    $method=$_SERVER['REQUEST_METHOD']??'';
    if ($method==='POST' && (int)($_SERVER['CONTENT_LENGTH']??0)>16000) {
        http_response_code(413);echo json_encode(['ok'=>false,'message'=>'El mensaje es demasiado largo.']);exit;
    }
    if ($method==='POST' && strtolower(explode(';',$_SERVER['CONTENT_TYPE']??'')[0])!=='application/json') {
        http_response_code(415);echo json_encode(['ok'=>false,'message'=>'Formato no permitido.']);exit;
    }
    [$code,$response]=glix_process($method,$origin,(string)file_get_contents('php://input',false,null,0,16001),$_SERVER['REMOTE_ADDR']??'', $directory,
        static function(string $reply,string $body): bool {
            return mail('info@glixerp.com','Nueva consulta web - GLIX',chunk_split(base64_encode($body),76,"\r\n"),[
                'From'=>'GLIX Web <info@glixerp.com>',
                'Reply-To'=>$reply,
                'MIME-Version'=>'1.0',
                'Content-Type'=>'text/plain; charset=UTF-8',
                'Content-Transfer-Encoding'=>'base64'
            ],'-finfo@glixerp.com');
        });
    http_response_code($code);
    if ($code===429) header('Retry-After: 3600');
    if ($code!==204) echo json_encode($response,JSON_UNESCAPED_UNICODE|JSON_THROW_ON_ERROR);
} catch (Throwable $error) {
    error_log('GLIX contact service failure: '.get_class($error));
    http_response_code(503);
    echo json_encode(['ok'=>false,'message'=>'No pudimos conectar el formulario. Escribinos a info@glixerp.com.']);
}
