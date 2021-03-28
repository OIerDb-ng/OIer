<?php

// config.php

$config = array(
    'db_type' => "mysql",     //数据库类型
    'db_host' => '127.0.0.1', //数据库主机名
    'db_port' => 3306,
    'db_name' => 'oier', //使用的数据库
    'db_user' => 'root',      //数据库连接用户名
    'db_passwd' => 'root',   //对应的密码
);


// utils.php

function get_database_connection(): mysqli
{
    global $config;
    $conn = new mysqli(
        $config['db_host'], $config['db_user'], $config['db_passwd'], $config['db_name'], $config['db_port']
    );
    if ($conn->connect_error) die('Could not connect: ' . $conn->connect_error);
    $conn->set_charset("utf8");
    return $conn;
}
