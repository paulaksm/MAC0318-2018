# Instruções para uso do Git na MAC0318

O repositório oficial da disciplina está no GitHub com o nome [MAC0318-2018](https://github.com/paulaksm/MAC0318-2018).

Cada aluno deverá ter uma cópia do repositório para fins de versionamento do seus códigos ao longo da disciplina. Portanto, o primeiro passo deverá ser um __fork__ do reposítório-base.

Uma vez com uma cópia do repositório em sua conta, é possível criar uma instância _local_ deste repositório na qual serão realizadas mudanças nos códigos e criação de novos arquivos, que poderão por sua vez, ser enviados a instância _remota_ do mesmo repositório. 

##### Clonando o repositório

O repositório será clonado por padrão na pasta `MAC0318-2018` no caminho em que o comando foi executado. Substitua <nome_usuario> pelo seu nome de usuário no GitHub.
```
git clone https://github.com/<nome_usuario>/MAC0318-2018.git
```

##### Adicionando o repositório-base como upstream

A fim de acompanhar as mudanças realizadas no repositório-base, é necessário configurar o repositório para _upstream_ da sua cópia:
```
git remote add upstream https://github.com/paulaksm/MAC0318-2018.git
``` 

A operação poder ser verificada com:
``` 
git remote -v
```

##### Mantendo sua cópia atualizada com o repositório-base

Com a referência ao _upstream_ adicionada, é possível manter a cópia do repositório atualizada com os últimos _commits_ realizados no repositório-base.

``` 
git pull upstream master --rebase
```

É possível que a operação acima não seja realizada devido a conflitos entre o repositório _local_ e _remoto_, por exemplo, modificações locais que não foram adicionadas para _commit_.

Uma opção possível para este caso seria usar o commando _stash_ para salvar as modificações locais, viabilizando o _pull_ do upstream. **Atenção**: mesmo fazendo o _stash_, ainda pode ser necessário resolver conflitos de códigos que sofreram alterações entre _commits_.

```
git stash 
```

Depois de realizar o comando _pull_, é possível recuperar as mudanças locais salvas pelo _stash_ com:
```
git stash pop
```

##### Trabalhando com branches

Em um projeto de software, muitas vezes, várias pessoas irão alterar os mesmos arquivos de código. Para que isso seja possível, é necessário que cada desenvolvedor possa ter uma versão isolada da aplicação,
ou seja, uma versão do software que não é afetada pela modificação dos outros. Para resolver tal problema, uma boa prática é o uso de _branches_. Essa abordagem também é muito útil quando se deseja manter
uma versão estável do projeto, pois tal versão pode ficar em uma branch separada. Para criar uma branch, pode-se usar os seguintes comandos

```
git branch branchname     # cria a branch com o nome branchname
git checkout branchname   # muda o HEAD para a branch de nome branchname
```

Lembrando que o comando acima cria uma _branch_ com base na _branch_ em que o comando foi executado.

#### Referências
Esse tutorial de maneira alguma almeja detalhar a estrutura e comandos de sistemas de versionamento, apenas busca nortear os alunos da disciplina em comandos importantes e direcioná-los na busca por soluções.

[Learn X in Y minutes: where X=git](https://learnxinyminutes.com/docs/git/)

Um guia com comandos básicos está disponível em: https://github.com/juanfrans/GSAPP-AP/wiki/Github-Basic-Commands-(Terminal)

[Git cheat sheet](https://gist.github.com/hofmannsven/6814451)
