  <?php
/*----------------------------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------Conexão_BD-----------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/
/*Conexão com a BD*/
$servername = "---------------";
$username = "-------------------";
$password = "------------------";
$dbname = "-------------------";

/*Cria o $conn para ser utilizado quando criar uma conexão à BD*/
$conn = new mysqli($servername, $username, $password, $dbname);

/* Inicia a sessão */
session_start();

/*----------------------------------------------------------------------------------------------------------------------------*/
/*------------------------------------------------VerificaAconexão------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/

if ($conn->connect_error) {

    die("Falha na conexão: " . $conn->connect_error);
    }


/*----------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------BuscarAsRespostarAoFormulário-------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/

if ($_SERVER["REQUEST_METHOD"] == "POST")  /* Verifica se o método de solicitação HTTP é POST */
{
$PrimeiroNome = $_POST['PrimeiroNome']; /*Atribui à váriavél $PrimeiroNome o PrimeiroNome*/
$UltimoNome = $_POST['UltimoNome']; /*Atribui à váriavél $UltimoNome o ultimo nome*/
$email = $_POST['email']; /*Atribui à váriavél $email o email*/
$Password = $_POST['Password']; /*Atribui à váriavél $emailCliente a password*/

/* Transforma a password numa password encriptada usando o md5*/
$EncryptedPassword = md5($Password);

/* Consulta para obter o próximo IDcliente disponível*/
$sql = "SELECT MAX(IDcliente) AS max_id FROM Cliente";
$result = $conn->query($sql);

if ($result->num_rows > 0) { /*Verifica se o número de linhas do resultado é maior que 0*/
$row = $result->fetch_assoc(); /*Enquanto houver linhas, atribui a linha atual à variável $row*/
/* adiciona sempre 1 ao IDcliente*/
$next_id = $row["max_id"] + 1;
} 
else
{
/* E se não houver registros, começa com 1*/
$next_id = 1;
}


/* Insere na base de dados, utilizando os valores dados acima*/
$sql = "INSERT INTO Cliente (IDcliente, PrimeiroNome, UltimoNome, email, Password)
VALUES ( $next_id, '$PrimeiroNome', '$UltimoNome', '$email','$EncryptedPassword' )";


if ($conn->query($sql) === TRUE) /*Verifica se a query foi bem sucedida*/
{
echo "Conta criada";/*Diz se a conta foi criada com sucesso*/ 
    /*Botão de voltar, que redireciona para a página do formulário*/
echo '<form action="https://tgei21.epvr4.net/" method="get">
    <button type="submit">Voltar</button>
</form>'; 
} 
else 
{
/* Redireciona o user para uma página a dizer que houve um erro */

echo "erro";

}

}
$conn->close();
?>

