  ### What I Learned:
-     PHP
-     HTML, CSS & JavaScript (entry-level)
-     cPanel (WebServer configuration)
-     WordPress WebServer front-end configuration
-     MySQL & SQL
-     Cyber Security (contra MySQL Injections)
-     Relational Databases design & configuration


  ### Skills Improved:
-     Communication 
-     Time management 
-     Attention to Detail
-     Teamwork
  

  ### Softwares/Tools/Code Languages Used:
-     FileZilla Client
-     cPanel
-     WordPress
-     phpMyAdmin
-     MySQL Database
-     Visual Studio Code
-     PHP
-     HTML/CSS & JavaScript
-     SQL
-     Tidio AI (WordPress Plug-in)


# GPTBOX Overview
This project, done in the context of PAP, consisted of developing a WebApp, that has the objective of helping clients that need to store/transport objects reach companies in the storage and transport regime.
The clients that want to use our services need to be registered in our database and they can do so through one of the pages on the website, to access the form to know the companies they need to log in.
The website is hosted in a WebServer and on a portable XAMPP configured by us.

To do this I needed to develop a WebApp down to the configuration of the WebServer to the development of Relational Databases, FTP Accounts, Frontend & Backend.
This project had 3 Server so I needed to migrate the Databases to each server.

## Configuration of the WebServer
To configure the WebServer I used cPanel, a tool used when the SO is Linux, and with this tool I've created Databases, MySQL Users & FTP Accounts.

## Database
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/c2d847f7-408e-48f3-b2b8-1be5598ab6c7)

#### phpMyAdmin used to overview and configure tables

## WordPress
For the development of the WebApp itself I used WordPress because the focus wasn't to build a strong Frontend with HTML, CSS & JavaScript but to build a strong and secure Backend so the users can use the forms in a safe environment.
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/6d0b79fe-9567-4a19-9ed1-c3fe07654cad)

## HTML, CSS & JavaScript (Entrylevel)
For the forms I used HTML, CSS & JavaScript.
HTMl for the form itself
CSS for the interactive buttons
JavaScript for the pop-up confirmation when submitting a form

## PHP
The backend of this WebApp is very secure and on a safe environment, the passwords are encripted to protect the data of the users and on the Database all that relations that are made are by IDs.
Given that this WebApp has some pages it has a total of 4 PHP files to login, change passwords, the form itself and to signup.

First, I created an connection to the database
```php
<?php
$servername = "---------------";
$username = "-------------------";
$password = "------------------";
$dbname = "-------------------";

/*Cria o $conn para ser utilizado quando criar uma conexão à BD*/
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}
```

To get the form response I needed to do a REQUEST_METHOD via POST:
```php
if ($_SERVER["REQUEST_METHOD"] == "POST") { /* Verifica se o método de solicitação HTTP é POST */
  $emailCliente = $_POST['EmailCliente']; /*Atribui à váriavél $emailCliente o email*/
  $material = $_POST['material']; /*Atribui à váriavél $material o material*/
  $medidas = $_POST['medidas']; /*Atribui à váriavél $medidas as medidas*/
  $tipo = $_POST['tipo']; /*Atribui à váriavél $tipo o tipo*/
}
```

Then I needed to to a query to the SQL Database, first to create an package I needed the ID of the client and the ID of the company 
```php
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
```
If the client has an account it shows the Companies data:
```php
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
```

Then it grabs the ID of the company and creates and package on another table with the ID of the client and the ID of the company:
```php
  
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
```

Then it closes the connection to the database:
```php
$conn->close();/*Fecha a conexão à BD*/
?>
```

## CyberSecurity Agains SQL Injections
The Database is protected agains SQL injections by using a user with less permissions so it can't delete or change data that he isn't suposed to.



# Execution Timetable
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/31acdb35-0887-4787-b577-01d120b45434)

# Results
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/65a9401c-2201-4fac-8663-c59e06c11ade)
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/7e1697fe-ef76-4398-b343-684e5cf2db58)
In case of incorrect password or username:


![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/f05208f3-52f2-402b-8947-a9819bcebfb6)


Signup:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/a685dec2-20b1-41ea-8548-cc350a8ddf2f)
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/0cf392ec-d678-48cf-8473-2c8c1cd9c939)
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/67f969dc-5a5d-4b3c-9baa-ce60ca5581b2)


Encrypted password:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/68727ef7-d90c-4d42-abba-f1d7c593be07)

The Form:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/298f9fa2-9520-4542-b16f-3aaf33b58dd4)
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/8e00d6a9-46cf-4910-a01b-2f782a7d0995)

JavaScript PopUp:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/34507119-6454-478d-b77b-7713a59109b6)

Output:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/c4621798-941e-4540-93fd-5a1ced419156)

Change password:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/6e699d3e-505f-435a-9d3d-fd6528264803)
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/b0505e2b-453d-4b9d-913d-4fb03abc24f8)
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/cd36f37f-2e73-4ef9-ac6d-9b6ba0f9c046)

Result:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/c7dee0f6-55fa-42ee-8b30-1ab9e7b673d7)
![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/a8dcc330-97b4-4031-80c3-ae6fa9d9d122)


# Portable XAMPP:
Form:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/92df492f-748e-4474-87ec-13e7c454eca0)

JavaScript PopUp:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/b13e2cc2-d863-4c38-b54e-fe90a74cda3c)

Output:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/f907e947-76bc-42ee-93bb-8a1194327f43)

Login:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/73e17c95-a11a-47a6-9c6b-545de944fe05)

Menu:

![image](https://github.com/Bolofofopt/ProjetosC/assets/145719526/d0ca304c-3573-4632-b824-e1b7ee7d9bd7)
