## Tutorial pull-requests MAC0318-2018

A disciplina MAC0318 do IME-USP permite aos alunos contribuírem com seus projetos no repositório da disciplina. Cada aluno possui uma cópia do repositório, realizada através do  _fork_ no repositório-base.
Isso possibilita que mudanças realizadas nestas cópias sejam enviadas para o repositório-base.

Neste tutorial será detalhada a forma correta de contribuir na pasta __projetos__ do repostório MAC0318-2018.

#### 1. Realizar um commit final no arquivo que será enviado
Exemplo - Arquivo Localizacao.java foi escolhido para fazer parte dos projetos da disciplina no diretório projetos/Localizacao1D/ 
```
git add Localizacao.java
git commit -m "Adicionando versao final do arquivo para o pull-request"
```

#### 2. Criar branch com base na master do repositório da disciplina
Substitua <branchname> pelo nome do branch que preferir.
```
git checkout upstream/master -b <branchname>
```

#### 3. Localizar ID do commit final do arquivo
```
git log
```
Exemplo de retorno do comando acima:
```
commit f8095863d460eb36d7310b97d3ec9c32d9e65b21 (HEAD -> aluno1)
Author: paulaksm <paulaksm@ime.usp.br>
Date:   Fri Mar 16 15:02:55 2018 -0300

    final
```
Nesse caso o commit realizado por paulaksm com a mensagem "final" tem o ID `f8095863d460eb36d7310b97d3ec9c32d9e65b21`

#### 4. Selecionar um commit de uma branch e dar "recommit" em outra branch

Na _branch_ recém criada, execute o comando:
```
git cherry-pick <branch_em_que_o_commit_foi_realizado> <ID_do_commit>
```
Exemplo do comando cherry-pick usando os dados do exemplo anterior:
```
git cherry-pick aluno1 f8095863d460eb36d7310b97d3ec9c32d9e65b21
```

Caso alguma mensagem de erro apareça, execute o comando (substitua <nome_do_arquivo> pelo nome do arquivo a ser enviado):
```
git add <nome_do_arquivo>
git cherry-pick --continue
```

Nessa sequência, garantimos que a nova branch criada com base na `upstream/master` está exatamente igual ao repositório-base da disciplina, porém com um único arquivo a mais relacionado ao commit final.

#### 5. Abrindo um pull-request da nova branch

No browser, navegue até o seu repositório da disciplina e clique em `New pull request`.

Verifique se o base fork e a base estão corretos: paulaksm/MAC0318-2018 base: master

Verifique se o head fork está correto: <seu_usuario>/MAC0318-2018

E ao lado do head fork no campo `compare` selecione a nova branch, na qual realizamos as operações.

Feito isso, clique em `Create pull request` e prossiga com a operação.


#### Referências
[git cherry-pick](https://git-scm.com/docs/git-cherry-pick)
[Understanding the GitHub flow](https://guides.github.com/introduction/flow/)
