<?php
$servername = "localhost";
$username = "admin";
$password = "adminPassword";
$dbname = "mtgei21epvr_grupo02_DB";

/* Cria uma nova conexão MySQLi. As variáveis $servername, $username, $password e $dbname foram definidas anteriormente */
$conn = new mysqli($servername, $username, $password, $dbname);

/* Inicia uma nova sessão ou continua a sessão existente */
session_start();

/* Verifica se a conexão foi bem-sucedida. Se houver um erro de conexão, termina a execução do script */
if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

/* Verifica se o método de solicitação HTTP é POST */
if ($_SERVER["REQUEST_METHOD"] == "POST") 
{
  /* Recupera os valores dos campos de entrada do formulário */
  $PrimeiroNome = $_POST['PrimeiroNome'];
  $UltimoNome = $_POST['UltimoNome'];
  $email = $_POST['email'];
  $Password = $_POST['Password'];

  /* Transforma a password numa password encriptada usando o md5*/
  $EncryptedPassword = md5($Password);

  /* Consulta SQL para obter o maior IDcliente da tabela Cliente */
  $sql = "SELECT MAX(IDcliente) AS max_id FROM Cliente";
  $result = $conn->query($sql);

  /* Verifica se a consulta retornou algum resultado */
  if ($result->num_rows > 0) {
      /* Recupera a linha de resultado como uma matriz associativa */
      $row = $result->fetch_assoc();
      /* Incrementa o valor máximo de IDcliente para obter o próximo ID */
      $next_id = $row["max_id"] + 1;
  } 
  else
  {
      /* Se não houver registros na tabela, define o próximo ID como 1 */
      $next_id = 1;
  }
   
  /* Query SQL para inserir o novo cliente na tabela Cliente */
  $sql = "INSERT INTO Cliente (IDcliente, PrimeiroNome, UltimoNome, email, Password)
  VALUES ( $next_id, '$PrimeiroNome', '$UltimoNome', '$email','$EncryptedPassword' )";
  
  /* Executa a Query SQL e verifica se foi bem-sucedida */
  if ($conn->query($sql) === TRUE) 
  {
    /* Se a consulta foi bem-sucedida, imprime uma mensagem de sucesso */
    echo "Conta criada";
    /* Cria uma nova página HTML para o usuer no diretório htdocs, com a permissão de escrita (w) */
    $user_page = fopen("E:\\xampp\htdocs\PAP_XAMPP\Users\\$email.html", "w");
    /* Define o conteúdo da nova página HTML */
    $html_content = "<h1>Bem vindo, $email</h1>";
    $html_content .= "<a href='https://127.0.0.1/PAP_XAMPP/MenuXAMPP.html'><button>Voltar para o Menu</button></a>";
    $html_content .= "<a href='https://127.0.0.1/PAP_XAMPP/form.html'><button>Formulario</button></a>";
    /* Escreve o conteúdo na nova página HTML */
    fwrite($user_page, $html_content);
    /* Fecha o arquivo da nova página HTML */
    fclose($user_page);
  } 
  else 
  {
    /* Se a consulta falhou, imprime uma mensagem de erro */
    echo "erro";
  }
}
/* Fecha a conexão MySQLi */
$conn->close();
?>