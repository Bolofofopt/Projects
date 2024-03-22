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

/*----------------------------------------------------------------------------------------------------------------------------*/
/*------------------------------------------------VerificaAconexão------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/

if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

/*----------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------BuscarAsRespostarAoFormulário-------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/


if ($_SERVER["REQUEST_METHOD"] == "POST") { /* Verifica se o método de solicitação HTTP é POST */
  $emailCliente = $_POST['EmailCliente']; /*Atribui à váriavél $emailCliente o email*/
  $material = $_POST['material']; /*Atribui à váriavél $material o material*/
  $medidas = $_POST['medidas']; /*Atribui à váriavél $medidas as medidas*/
  $tipo = $_POST['tipo']; /*Atribui à váriavél $tipo o tipo*/
}



/*----------------------------------------------------------------------------------------------------------------------------*/
/*------------------------------------------SelectDoCliente-------------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/
/*Procura na Base de dados um cliente com o nome colocado no formulário*/
$sql = "SELECT Cliente.IDcliente, Cliente.PrimeiroNome FROM Cliente WHERE Cliente.Email  = '$emailCliente'";
/*Consulta SQL é executada como query(), utilizamos o objeto de conexão à BD $conn, o resultado é guardado 
na varavél $result*/
$result = $conn->query($sql);

$nomeCliente = ""; /*Inicialia a variável*/

if ($result->num_rows > 0) { /*Verifica se o número de linhas do resultado é maior que 0*/
  while($row = $result->fetch_assoc()) { /*Enquanto houver linhas, atribui a linha atual à variável $row*/
    $idCliente = $row["IDcliente"]; /*Atribui o valor da coluna IDcliente à variável $idCliente*/
    $nomeCliente = $row["PrimeiroNome"]; /*Atribuir o nome do cliente à variável criada antes*/
  }
} else {
 header("Location: https://tgei21.epvr4.net/erro/"); /*Redireciona para uma página de erro*/
}
/*Botão de voltar, que redireciona para a página do formulário*/
echo '<form action="https://tgei21.epvr4.net/formulario/" method="get">
        <button type="submit">Voltar</button>
      </form>';
/*----------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------OutputDoFornecedor------------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/
/*Consulta SQL, seleciona o nome, o email e a morada da tabela Fornecedor, onde filtra os dados para saber
qual fornecedor tem os dados de acordo com o que o cliente respondeu no formulário, variavéis $material e 
$medidas*/

$sql = "SELECT Fornecedor.NomeFornecedor, Fornecedor.EmailFornecedor, Fornecedor.MoradaFornecedor FROM Fornecedor 
        JOIN caixas ON Fornecedor.IDcaixa = caixas.IDcaixa
        JOIN TipoDeCaixa ON caixas.IDtipodecaixa = TipoDeCaixa.IDtipodecaixa 
        WHERE TipoDeCaixa.colDescricaoCaixa = '$material' AND caixas.Medidas = '$medidas' AND Fornecedor.tipo = '$tipo';";
/*Consulta SQL é executada como query(), utilizamos o objeto de conexão à BD $conn, o resultado é guardado 
na varavél $result*/
$result = $conn->query($sql);

$nomeFornecedor = ""; /*Inicialia a variável*/

if ($result->num_rows > 0) { /*Verifica se o número de linhas é maior que 0*/
  while($row = $result->fetch_assoc()) { /*Enquanto houver linhas, atribui a linha atual à variável $row*/
    echo "<br>"; /*Quebra de linha*/
    echo "Nome do Fornecedor: " . $row["NomeFornecedor"]. "<br>"; /*Output dos dados do fornecedor*/
    echo "Email do Fornecedor: " . $row["EmailFornecedor"]. "<br>"; /*Output dos dados do fornecedor*/
    echo "Morada do Fornecedor: " . $row["MoradaFornecedor"]. "<br>"; /*Output dos dados do fornecedor*/
    $nomeFornecedor = $row["NomeFornecedor"]; /*Atribui o nome do fornecedor à variável criada anteriormente*/
  }
} else {
  echo "Nenhum resultado encontrado"; /*Avisa se não houver fornecedores encontrados*/
}

/*----------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------InsertNaTabelaEncomenda-------------------------------------------------------------*/
/*----------------------------------------------------------------------------------------------------------------------------*/

/*Procura o ID do fornecedor que têm o nome do último fornecedor colocado no output dos dados*/
$sql = "SELECT Fornecedor.IDfornecedor FROM Fornecedor WHERE Fornecedor.NomeFornecedor = '$nomeFornecedor'";
/*Consulta SQL é executada como query(), utilizamos o objeto de conexão à BD $conn, o resultado é guardado 
na varavél $result*/
$result = $conn->query($sql);

if ($result->num_rows > 0) { /*Verifica se o número de linhas é maior que 0*/
  while($row = $result->fetch_assoc()) { /*Enquanto houver linhas, atribui a linha atual à variável $row*/
    $idFornecedor = $row["IDfornecedor"]; /* Atribui o valor da coluna 'IDfornecedor' da linha atual à variável $idFornecedor */
  }
} else {
  echo "Nenhum fornecedor encontrado";/*Avisa se não houver fornecedores encontrados*/
}

/* Criar um novo IDEncomenda*/

/* Buscar o maior IDencomenda atual*/
$sql = "SELECT MAX(IDencomenda) as max_id FROM Encomenda";
$result = $conn->query($sql);

$next_id = 1; /*Inicia com 1*/

if ($result->num_rows > 0) { /*Verifica se o número de linhas é maior que 0*/
  $row = $result->fetch_assoc(); /*Enquanto houver linhas, atribui a linha atual à variável $row*/
  $next_id = $row["max_id"] + 1; /*Adiciona +1 quando deteta que existe o ID*/
}


/*Insere a encomenda*/
$sql = "INSERT INTO Encomenda (IDfornecedor, IDcliente, IDencomenda) VALUES ('$idFornecedor', '$idCliente', '$next_id')";

if ($conn->query($sql) === TRUE) { /*Verifica se a consulta SQL foi bem sucedida*/
    /*Confirma que a encomenda foi adicionada e diz o ID*/
    echo "Nova encomenda criada com sucesso. O número da encomenda é: " . $next_id;

} 
else 
{
  header("Location: https://tgei21.epvr4.net/erro/ "); /*Redireciona para uma página de erro*/
}

$conn->close();/*Fecha a conexão à BD*/
?>