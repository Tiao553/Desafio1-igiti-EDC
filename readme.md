# Desafio 1 - IGTI : Instanciando uma pipeline toda com IAC

## Falando um pouco da sobre a IGTI

Uma instituição de ensino online e presencial que tem como missão a melhor formação em TI para todos. **Entregando Bootcamps, graduação, pós-graduação, imersões internacionais e até um Radar de Oportunidades para impulsionar a sua carreira.** Uma formação completa e especializada a preços acessíveis, com a qualidade e a inovação que só o IGTI oferece. 

>  Para mais informações acesse ao [site](https://www.igti.com.br/).

---

## Vamos ao desafio
 O desafio propotos em cada um dos módulos da IGTI tem como objetivo realizar alguma aplicação com a finalidade de responder certas perguntas. **Neste repositório vamos alocar apenas a construção da arquitetura para responder as perguntas.**

### O desafio

Você deve fazer a ingestão do Censo Escolar 2020 em uma estrutura de Data Lake na AWS (ou em outro provedor de sua escolha). Depois disso, você deve utilizar alguma tecnologia de Big Data para converter os dados para o formato parquet. Em seguida, disponibilize os dados para consulta no AWS Athena (ou outra engine de Data Lake de outra nuvem ou no BigQuery, no caso do Google Cloud) e faça uma consulta para demonstrar a disponibilidade dos dados. Por fim, utilize a ferramenta de Big Data ou a engine de Data Lake para realizar investigações nos dados e responder às perguntas do desafio.

### Hands on

Para construir esta arquitetura vamos utilizar as seguintes ferramentas:

* Provedor cloud: **AWS**
* Liguagem de desenvolvimento de Infraestrutura como código: **Terraform**
* Orquestrador de tarefas: **Airflow**
* Liguagem de gerenciamento dos dados: **Python**

Ao avaliar o desafio foi decido a construção da seguinte arquitetura para atender ingerir processar e servir esses dados para responder as perguntas propostas:

<center><img src='img/Untitled Diagram.png'></center>

### Dificuldades encontradas

Algumas coisas precisaram ser feitas manuais, como a criação da role para o sagemaker, assim como a key pair do ec2 para utilização de alguns serviços.

### Principais ganhos da arquitetura

Como o airflow é instanciado em uma maquina na AWS qualquer pessoa, com acesso, pode gerencia-la de forma remoto.
