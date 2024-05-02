

<?php


// Conexão com a BD ( usando a conta de cliente, que tem apenas acesso a ver as tabelas)
$servername = "-------------------";
$username = "-------------------";
$password = "-------------------";
$dbname = "-------------------";

$conn = new mysqli($servername, $username, $password, $dbname);

/* Inicia a sessão */
session_start();

/* Verifica a conexão */
if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $Password = $_POST['Password'];

    /* Encripta a passowrd com o md5 ( método de encriptação message-digest) */
    $EncryptedPassword = md5($Password);

    /* Prepara a query para verificar se o email e a senha estão corretos */
    $stmt = $conn->prepare("SELECT * FROM Cliente WHERE email = ? AND Password = ?");
    $stmt->bind_param("ss", $email, $EncryptedPassword);
    /* Usámos bind_param() para vincular as variáveis $email e $EncryptedPassword na consulta SQL. 
    'ss' significa que as variáveis são strings. */

    /* Executa a consulta */
    $stmt->execute();

    /* Obtém o resultado */
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        /* Se o email e password estiverem corretos, inicia a sessão */
        $_SESSION['loggedin'] = true;
        $_SESSION['email'] = $email;

        /* Redireciona para a página HTML específica do user*/
        header("Location: https://127.0.0.1/PAP_XAMPP/Users/$email.html");
        exit;
    } else {
        /* Se o email ou a senha estiverem incorretos, mostra uma mensagem de erro */
        echo "Password ou email errados";
    }

    /* Fecha a declaração */
    $stmt->close();
}
$conn->close(); /* fecha a conexão */
?>
