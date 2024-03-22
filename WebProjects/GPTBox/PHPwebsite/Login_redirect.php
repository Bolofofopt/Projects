<?php


/* Conexão com a BD ( usando a conta de cliente, que tem apenas acesso a ver as tabelas) */
$servername = "---------------";
$username = "-------------------";
$password = "------------------";
$dbname = "-------------------";




/* Cria conexão */
$conn = new mysqli($servername, $username, $password, $dbname);

/* Inicia a sessão */
session_start();

/* Verifica a conexão */
if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}
/* Verifica se o método de requisição é POST */
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email']; /* Armazena o email enviado pelo user */
    $Password = $_POST['Password']; /* Armazena a password enviada pelo user */

    /* Encripta a passowrd com o md5 ( método de encriptação message-digest) */
    $EncryptedPassword = md5($Password);

    /* Prepara a query para verificar se o email e a senha estão corretos */
    $stmt = $conn->prepare("SELECT * FROM Cliente WHERE email = ? AND Password = ?");
    $stmt->bind_param("ss", $email, $EncryptedPassword);  /*Esta linha está a vincular os parametros à declaração SQL preparada.
    ss significa que são 2 strings. O $email e $EncryptedPassword, são as variáveis que contêm os valores reais que serão usados no lugar dos placeholders (?) na declaração SQL. Fizemos isto para evitar SQL injections */
    

    /* Executa a consulta */
    $stmt->execute();

    /* Obtém o resultado */
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        /* Se o email e password estiverem corretos, inicia a sessão */
        $_SESSION['loggedin'] = true;
        $_SESSION['email'] = $email;

        /* Redireciona o user para a página do menu */
        header("Location: https://tgei21.epvr4.net/menu/");
        exit;

    } else {
        /* Se o email ou a senha estiverem incorretos, mostra uma mensagem de erro */
          header("Location: https://tgei21.epvr4.net/dados-incorretos/");
    }

    /* Fecha a declaração */
    $stmt->close();
}
$conn->close();
?>