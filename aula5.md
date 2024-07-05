# Tópicos avançados e Implantação
- vamos utilizar a cloud da AWS

## para começar
- acesse o link: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html para baixar o arquivo instalador da aws CLI.
- para verificar se deu certo a instalação, abra seu terminal e digite: aws
- se aparecer sugestões de comando como esses:

        usage: aws [options] <command> <subcommand> [<subcommand> ...] [parameters]
        To see help text, you can run:

        aws help
        aws <command> help
        aws <command> <subcommand> help

        aws: error: the following arguments are required: command
    
é porque já está funcionando

## Criando autenticação para criar nosso serviço na AWS
- pesquise no console da AWS: IAM
- vá em Users(usuários)
- criar usuário
- dê um nome ao usuário
- selecione as permissões que via dar para o usuário (de preferencia dê o mínimo de permissões possísveis)
- agora scrollando pra baixo procure por *AdministratorAccess* e marque essa caixinha
- clique em next
- crie uma tag se quiser e em seguida criar usuário
- após criar o usuário, ele vai aparecer na tela de gerencieamento, clique nele e vá em credenciais de segurança
- agora crie uma access Key
- selecione CLI
- confirme a caixinha -> next
- crie uma tag se quiser e cliqueem criar chave de acesso
- ao fazer isso, ele vai dar duas informações:
    - a Access key
    - e a Secret access key
- salve essas chaves e NÃO COMPARTILHE COM NINGUÉM

## Configurando a AWS CLI
- de volta ao terminal digite: aws configure
- ele vai pedir a access Key e em seguida Secret Access Key a região e output format
- agora para saber as linhas de comandos, basta pesquisar no google: aws cli e nome do serviço que vc quiser. Ex: aws cli beanstalk

## Instalando a EB CLI

