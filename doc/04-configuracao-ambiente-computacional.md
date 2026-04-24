IFTO / UAB - Campus Araguatins

# Curso de pós-graduação lato sensu em Desenvolvimento de Sistemas Computacionais

# Discipina Desenvolvimento Web

# Aula 05 - 22/04/2026



# Tutorial para Implantação do Ambiente Computacional

## 1. Plataforma: Sistema operacional Ubuntu no Windows Subsystem for Linux (WSL)



## 2. Visualizar instalações Linux sobre WSL:

```

C:\>wsl -l -v
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2

```

## 3. Implantar nova instalaçã Linux no WSL:

Definir o WSL 2 como padrão

```
C:\>wsl --set-default-version 2
```

Listar distribuições Linux disponíveis para instalação:

```
C:\>wsl --list --online
Veja a seguir uma lista de distribuições válidas que podem ser instaladas.
Instale usando 'wsl.exe --install <Distro>'.
NAME                            FRIENDLY NAME
AlmaLinux-8                     AlmaLinux OS 8
AlmaLinux-9                     AlmaLinux OS 9
AlmaLinux-Kitten-10             AlmaLinux OS Kitten 10
AlmaLinux-10                    AlmaLinux OS 10
Debian                          Debian GNU/Linux
FedoraLinux-43                  Fedora Linux 43
FedoraLinux-42                  Fedora Linux 42
SUSE-Linux-Enterprise-15-SP7    SUSE Linux Enterprise 15 SP7
SUSE-Linux-Enterprise-16.0      SUSE Linux Enterprise 16.0
Ubuntu                          Ubuntu
Ubuntu-24.04                    Ubuntu 24.04 LTS
Ubuntu-22.04                    Ubuntu 22.04 LTS
Ubuntu-20.04                    Ubuntu 20.04 LTS
archlinux                       Arch Linux
eLxr                            eLxr 12.12.0.0 GNU/Linux
kali-linux                      Kali Linux Rolling
openSUSE-Tumbleweed             openSUSE Tumbleweed
openSUSE-Leap-16.0              openSUSE Leap 16.0
OracleLinux_7_9                 Oracle Linux 7.9
OracleLinux_8_10                Oracle Linux 8.10
OracleLinux_9_5                 Oracle Linux 9.5
openSUSE-Leap-15.6              openSUSE Leap 15.6
SUSE-Linux-Enterprise-15-SP6    SUSE Linux Enterprise 15 SP6

```



Baixar e instalar o Ubuntu 24.04 LTS no WSL.

```
C:\>wsl --install -d Ubuntu-24.04
Baixando: Ubuntu 24.04 LTS
Instalando: Ubuntu 24.04 LTS

Distribuição instalada com êxito. Ele pode ser iniciado por meio de 'wsl.exe -d Ubuntu-24.04'

```

Renomear distribuição instalada (opcional):

```
#Criar pasta para backup:
C:\>mkdir C:\wsl

#Exportar instalação Ubuntu-24.04:
C:\>wsl --export Ubuntu-24.04 C:\wsl\ubuntu2404.tar
Exportação em andamento. Isso pode levar alguns minutos. (1190 MB)
A operação foi concluída com êxito.

#Remover instalação Ubuntu 24.04:
C:\>wsl --unregister Ubuntu-24.04
Cancelando.
A operação foi concluída com êxito.

#Importar instalação Ubuntu-24.04 renomeada:
#C:\>wsl --import <nome-da-distro> <diretorio-raiz> <arquivo-backup>
C:\>wsl --import UbuntuDevUAB C:\WSL\UbuntuDevUAB C:\WSL\ubuntu2404.tar
A operação foi concluída com êxito.

```

Selecionar instalação Linux UbuntuDevUAB

```
C:\>wsl -d UbuntuDevUAB
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 5.15.167.4-microsoft-standard-WSL2 x86_64)
 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro
 System information as of Tue Apr 21 19:09:05 -03 2026
  System load:  0.0                 Processes:             49
  Usage of /:   0.1% of 1006.85GB   Users logged in:       0
  Memory usage: 1%                  IPv4 address for eth0: 172.27.1.122
  Swap usage:   0%
This message is shown once a day. To disable it please create the
/root/.hushlogin file.

root@fabio-alien:/mnt/c#
```

A partir daqui você já estará operando na instalação Linux.

Atualizar pacotes da instalação Linux: 

```
root@fabio-alien:/mnt/c# sudo apt update && sudo apt upgrade -y
```



## 4. Configurar usuários no Linux:

```
#Definir senha do root:
root@fabio-alien:/mnt/c# passwd
New password:
Retype new password:
passwd: password updated successfully

#Adicionar usuário desenvolvedor:
root@fabio-alien:/mnt/c# adduser uab
info: Adding user `uab' ...
info: Selecting UID/GID from range 1000 to 59999 ...
info: Adding new group `uab' (1000) ...
info: Adding new user `uab' (1000) with group `uab (1000)' ...
info: Creating home directory `/home/uab' ...
info: Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for uab
Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] Y
info: Adding new user `uab' to supplemental / extra groups `users' ...
info: Adding user `uab' to group `users' ...

#Incluir usuário uab no grupo sudoers: 
root@fabio-alien:/mnt/c# pico /etc/sudoers
#Adicionar a seguinte linha no final do arquivo. 
#uab ALL=(ALL:ALL) ALL
#Use CTRL+X para sair, e salve as alterações. 

#Alternar usuário:
root@fabio-alien:/mnt/c# su - uab
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 5.15.167.4-microsoft-standard-WSL2 x86_64)
 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro
 System information as of Tue Apr 21 19:22:43 -03 2026
  System load:  0.0                 Processes:             30
  Usage of /:   0.1% of 1006.85GB   Users logged in:       1
  Memory usage: 1%                  IPv4 address for eth0: 172.27.1.122
  Swap usage:   0%
This message is shown once a day. To disable it please create the
/home/uab/.hushlogin file.

uab@fabio-alien:~$
```

## 5. Instalar Gemini CLI

```
#Instalar npm: 
uab@fabio-alien:~$ sudo apt install npm

#Baixar scripts de instalação do nvm:
uab@fabio-alien:~$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

#Reiniciar bash: 
uab@fabio-alien:~$ source ~/.bashrc

#Instalar nvm:
uab@fabio-alien:~$ nvm install 20

#Definir uso do nvm 20: 
uab@fabio-alien:~$ nvm use 20
Now using node v20.20.2 (npm v10.8.2)

#Instalar o Google Gemini CLI
uab@fabio-alien:~$ sudo npm install -g @google/gemini-cli


```

## 

    #Instalar o Docker para poder utilizar o modo sandbox: 
    uab@fabio-alien:~/projeto-uab$ sudo apt install docker.io -y
    
    #Adicionar usuário ao grupo Docker: 
    uab@fabio-alien:~/projeto-uab$ sudo usermod -aG docker $USER
    
    #Aplicar as alterações de configurações de usuários: 
    uab@fabio-alien:~/projeto-uab$ newgrp docker

## 

## 6. Copiar arquivos do projeto

Nesse ponto, você pode usar o Windows Explorer para copiar os arquivos do seu projeto para uma pasta da instalação Linux. De preferência, crie uma pasta na área do seu usuário. 

Nesse caso, como você fez a cópia com o Windows Explorer, pode ser que o proprietário da pasta seja o usuário root. Então execute o seguinte comando para alterar a propriedade da pasta para o usuário desenvolvedor: 

```
#sudo chown -R <usuario>:<grupo> <direitorio>
uab@fabio-alien:~$ sudo chown -R uab:uab projeto-uab
```



## 7. Iniciar Gemini CLI

    #Instalar o Docker para poder utilizar o modo sandbox: 
    uab@fabio-alien:~/projeto-uab$ sudo apt install docker.io -y
    
    #Adicionar usuário ao grupo Docker: 
    uab@fabio-alien:~/projeto-uab$ sudo usermod -aG docker $USER
    
    #Aplicar as alterações de configurações de usuários: 
    uab@fabio-alien:~/projeto-uab$ newgrp docker

```
#Iniciar Gemini no modo Sandbox: 
uab@fabio-alien:~/projeto-uab$ 
```

- Escolher pasta do projeto

- Autentique com conta Google institucional do IFTO

- Documentação do Gemini CLI: https://geminicli.com/docs/
  
  

## 8. Instalação do ambiente de desenvolvimento:

Para implantar o ambiente de desenvolviment inicial, aplique o seguinte prompt, com as devidas adequações e/ou complementos: 

```
Configure um ambiente de desenvolvimento completo e funcional para o projeto descrito no arquivo doc/03-especs.md. 
```



Para sincronizar o ambiente de desenvolvimento com o GitHub, use o seguinte prompt, com as devidas adequações e/ou complementos: 

```
Proceda as instalações e configurações necessárias para sincornização da pasta ~/projeto-uab com um repositório do GitHub chamado projeto-uab. O nome do usuário do GitHub é ****** e email *******@ifto.edu.br. 
```

- Crie um repositório no GitHub para receber o projeto.

- Acesse o site do GitHub para gerar um token. Para isso, clique na sua foto de perfil e depois acesse Settings > Developer Settings > Personal access tokens > Tokens. 

- Faça o upload inicial: 

- ```
  uab@fabio-alien:~/projeto-uab$ git remote set-url origin https://<SEU_TOKEN>@github.com/<SEU_USUARIO>/<SEU_REPOSITORIO>.git
  ```

- Para adicionar novos arquivos: 
  
  ```git
  uab@fabio-alien:~/projeto-uab$ git add .
  ```
  
  

- Para consolidar versões: 
  
  ```
  uab@fabio-alien:~/projeto-uab$ git commit -m "Descrição das alterações"
  ```

- Para sincronizar versão local com respositório remoto: 

```
uab@fabio-alien:~/projeto-uab$ git push https://<SEU_TOKEN>@github.com/<SEU_USUARIO>/<SEU_REPOSITORIO>.git main
```
