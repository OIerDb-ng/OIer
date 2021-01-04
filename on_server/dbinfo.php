<?php
class DbInfo
{
    const DBMS = "mysql";     //数据库类型
    const HOST = 'localhost:3308'; //数据库主机名
    const DBNAME = 'oier'; //使用的数据库
    const USER = 'root';      //数据库连接用户名
    const PASSWD = 'xsz123';    //对应的密码

    static function GetDbConnStr()
    {
         // $dsn = "$dbms:host=$host;dbname=$dbName";
        $dsn = self::DBMS . ":host=" . self::HOST . "; dbname=" . self::DBNAME;
        return ($dsn);
    }
    static function GetMysqlConn()
    {
        $conn=mysqli_connect(self::HOST, self::USER, self::PASSWD, self::DBNAME);
        return $conn;
    }
    function GetDbUser()
    {
        return (self::USER);
    }

    function GetDbPwd()
    {
        return (self::PASSWD);
    }
}
?>
