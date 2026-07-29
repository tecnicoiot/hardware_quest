# HardwareQuest - Jogo de Montagem de Hardware

Este jogo foi projetado e desenvolvido para ser executado no **Raspberry Pi**, servindo como projeto final do **Curso Livre de Robótica com Raspberry Pi** no **Senac Registro**. O objetivo do jogo é testar os conhecimentos de hardware do jogador através de um Quiz interativo e de um simulador de etapas de montagem (encaixe de peças nos slots adequados).

---

## 👥 Criadores do Projeto

*   **Igor Oliveira**  
    *Concepção e Criação Original*  
    Estudante do curso Técnico em IoT.  
    🔗 [GitHub Profile](https://github.com/igoroliveirs97)

*   **Túlio Zanella**  
    *Edição e Complemento do Jogo*  
    Estudante do curso Técnico em IoT.  
    🔗 [GitHub Profile](https://github.com/tzanella)

---

## 🍓 Como Executar no Raspberry Pi (Raspberry Pi OS / Debian)

### 1. Instalar as dependências do sistema
No Raspberry Pi OS, a forma mais rápida de instalar o Pygame para toda a máquina é usando o gerenciador de pacotes da distribuição:
```bash
sudo apt update
sudo apt install python3-pygame -y
```

### 2. Executar o jogo
Com o Pygame instalado, navegue até a pasta do projeto e execute:
```bash
python3 main.py
```

---

## 🔵 Como Executar e Compilar no Fedora Linux

### 1. Executar a partir do código-fonte (Interpretado)
Você pode rodar instalando as dependências do sistema via DNF:
```bash
sudo dnf install python3-pygame -y
python3 main.py
```

Ou usando um ambiente virtual e instalando as dependências listadas no `requirements.txt`:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### 2. Executar o binário compilado (AppImage / Standalone)
A versão do executável standalone empacotada para Linux x86_64 fica localizada na pasta `dist/`. Para executar diretamente:
```bash
chmod +x dist/HardwareQuest-x86_64.AppImage
./dist/HardwareQuest-x86_64.AppImage
```

### 3. Compilar usando o Makefile
Caso deseje gerar novos pacotes e binários:
- Gerar o executável nativo Linux e empacotar em AppImage x64:
  ```bash
  make linux-x64
  ```
- Gerar o executável `.exe` para Windows x64:
  ```bash
  make windows-x64
  ```
- Limpar os diretórios temporários de compilação:
  ```bash
  make clean
  ```

---

## ⚖️ Licença

Este projeto é distribuído sob os termos da **Licença MIT**. Veja os arquivos correspondentes para mais detalhes.
