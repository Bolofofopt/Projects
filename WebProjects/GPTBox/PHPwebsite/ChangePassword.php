<?php

$servername = "---------------";
$username = "-------------------";
$password = "------------------";
$dbname = "-------------------";

/* Cria uma nova conexão com a base de dados */
$conn = new mysqli($servername, $username, $password, $dbname);

/* Verifica se houve algum erro na conexão */
if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

/* Verifica se o método de requisição é POST */
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    /* Armazena o email enviado pelo user */
    $email = $_POST["email"];
    /* Armazena a senha antiga enviada pelo user após aplicar a função md5 */
    $old_password = md5($_POST["old_password"]);
    /* Armazena a nova senha enviada pelo user após aplicar a função md5 */
    $new_password = md5($_POST["new_password"]);
    /* Armazena a confirmação de senha enviada pelo user após aplicar a função md5 */
    $confirm_password = md5($_POST["confirm_password"]);

    /* Verifica se a nova senha é igual à confirmação de senha */
    if ($new_password != $confirm_password)
    {
        /* Se as senhas não coincidirem, redireciona o user para a página de erro */
        header("Location: https://tgei21.epvr4.net/erro-na-alteracao-de-palavra-passe/");
        exit;
    }

    /* Prepara a query SQL para verificar se o email e a senha antiga existem na BD */
    $sql = "SELECT * FROM Cliente WHERE Email = '$email' AND Password = '$old_password'";
    /* Executa a consulta SQL */
    $result = $conn->query($sql);

    /* Verifica se a query retornou algum resultado */

    if ($result->num_rows > 0) {
        /* Se o resultado for positivo, prepara a query SQL para atualizar a senha */
        $sql = "UPDATE Cliente SET password = '$new_password' WHERE email = '$email'";
        /* Executa a query SQL de update */
        if ($conn->query($sql) === TRUE) 
        {
            /* Se a query for executada com sucesso, redireciona o user para a página de sucesso */
            header("Location: https://tgei21.epvr4.net/alteracao-bem-sucedida/");
        }

    } else {
        /* Se o email ou a senha estiverem incorretos, redireciona o user para a página de erro */
        header("Location: https://tgei21.epvr4.net/erro-na-alteracao-de-palavra-passe/");
    }
   
}
/* Fecha a conexão com a base de dados */
$conn->close();
?>