import pygame
import random
import json
import os
import time

# ==========================================
# CONFIGURAÇÕES E INICIALIZAÇÃO
# ==========================================
pygame.init()
LARGURA, ALTURA = 950, 680
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hardware Master - Edição Binária")
relogio = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
VERDE_MATRIX = (0, 255, 70)
VERDE_ESCURO = (0, 100, 30)
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)
VERMELHO = (255, 60, 60)
AZUL_CLARO = (80, 180, 255)
CINZA_TRANSPARENTE = (10, 20, 10, 230)

# Fontes
FONTE_BINARIO = pygame.font.SysFont("monospace", 16, bold=True)
FONTE_TITULO = pygame.font.SysFont("arial", 28, bold=True)
FONTE_SUBTITULO = pygame.font.SysFont("arial", 20, bold=True)
FONTE_TEXTO = pygame.font.SysFont("arial", 16)
FONTE_MINI = pygame.font.SysFont("monospace", 13)

# ==========================================
# DATA: PERGUNTAS E PEÇAS
# ==========================================
QUIZ_DATA = [
    {
        "pergunta": "1. Qual componente é considerado o 'Cérebro' do computador?",
        "opcoes": ["Placa-Mãe", "Processador (CPU)", "Memória RAM", "Fonte (PSU)"],
        "correta": 1
    },
    {
        "pergunta": "2. Qual memória armazena dados temporários e é volátil?",
        "opcoes": ["Memória RAM", "HD / SSD", "Memória ROM / BIOS", "Cache da Placa de Vídeo"],
        "correta": 0
    },
    {
        "pergunta": "3. Se o HD está cheio, adicionar mais RAM aumenta o armazenamento?",
        "opcoes": ["Sim, RAM guarda arquivos", "Não, RAM é para velocidade/trabalho", "Sim, se for DDR5", "Depende do cooler"],
        "correta": 1
    },
    {
        "pergunta": "4. Onde a placa de vídeo dedicada (GPU) é conectada?",
        "opcoes": ["Soquete da CPU", "Slot PCIe x16", "Porta SATA 3", "Painel Frontal"],
        "correta": 1
    },
    {
        "pergunta": "5. Qual componente converte a corrente alternada para contínua?",
        "opcoes": ["Water Cooler", "Chipset", "Fonte de Alimentação (PSU)", "Bateria CR2032"],
        "correta": 2
    },
    {
        "pergunta": "6. Um PC sem processador consegue ligar e rodar jogos se tiver muita RAM?",
        "opcoes": ["Sim, a RAM roda jogos só", "Sim, se tiver SSD NVMe", "Não, a CPU é obrigatória", "Sim, via cabo HDMI"],
        "correta": 2
    },
    {
        "pergunta": "7. O que deve ser aplicado entre a CPU e o cooler para condução térmica?",
        "opcoes": ["Cola Quente", "Pasta Térmica", "Fita Isolante", "Óleo Mineral"],
        "correta": 1
    },
    {
        "pergunta": "8. Qual armazenamento usa memória flash sem partes mecânicas móveis?",
        "opcoes": ["HD Mecânico", "Leitor DVD", "Disquete", "Unidade SSD"],
        "correta": 3
    }
]

ENCAIXE_DATA = [
    {
        "id": "cpu",
        "nome": "Processador (CPU)",
        "alvo": "Soquete LGA/AM4",
        "motivo": "A CPU precisa ser travada diretamente no Soquete de Pinos da Placa-Mãe para processar os dados."
    },
    {
        "id": "ram",
        "nome": "Pente de Memória RAM",
        "alvo": "Slot DIMM RAM",
        "motivo": "A Memória RAM deve ser encaixada nos Slots DIMM laterais até ouvir o clique das travas."
    },
    {
        "id": "gpu",
        "nome": "Placa de Vídeo (GPU)",
        "alvo": "Slot PCIe x16",
        "motivo": "A GPU requer o barramento de alta velocidade do Slot PCIe x16 principal para transmitir vídeo."
    },
    {
        "id": "ssd",
        "nome": "SSD NVMe M.2",
        "alvo": "Slot M.2 NVMe",
        "motivo": "O SSD M.2 é parafusado diretamente na conexão dedicada M.2 para altíssimas taxas de leitura."
    },
    {
        "id": "psu_cable",
        "nome": "Cabo ATX 24 Pinos",
        "alvo": "Conector ATX 24P",
        "motivo": "O cabo principal de 24 Pinos da Fonte é o responsável por energizar os circuitos da Placa-Mãe."
    }
]

# ==========================================
# CLASSES DE SISTEMA
# ==========================================
class FundoBinario:
    def __init__(self, largura, altura, tamanho_fonte=18):
        self.largura = largura
        self.altura = altura
        self.tamanho_fonte = tamanho_fonte
        self.colunas = largura // tamanho_fonte
        self.gotas = [random.randint(-50, 0) for _ in range(self.colunas)]
        self.velocidades = [random.randint(1, 3) for _ in range(self.colunas)]

    def desenhar_e_atualizar(self, superficie):
        rastro = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        rastro.fill((0, 0, 0, 45))
        superficie.blit(rastro, (0, 0))

        for i in range(self.colunas):
            caractere = str(random.choice([0, 1]))
            x = i * self.tamanho_fonte
            y = self.gotas[i] * self.tamanho_fonte

            texto = FONTE_BINARIO.render(caractere, True, VERDE_MATRIX)
            superficie.blit(texto, (x, y))

            if y > self.altura and random.random() > 0.975:
                self.gotas[i] = 0
                self.velocidades[i] = random.randint(1, 3)

            self.gotas[i] += self.velocidades[i]


class PlacarGlobal:
    def __init__(self, arquivo="placar_global.json"):
        self.arquivo = arquivo
        self.pontuacoes = self.carregar_placar()

    def carregar_placar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def salvar_placar(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.pontuacoes, f, indent=4, ensure_ascii=False)

    def adicionar_pontuacao(self, nome, pontos):
        if not nome.strip():
            nome = "Jogador"
        self.pontuacoes.append({"nome": nome, "pontos": int(pontos)})
        self.pontuacoes = sorted(self.pontuacoes, key=lambda x: x["pontos"], reverse=True)[:10]
        self.salvar_placar()

    def desenhar(self, superficie, x, y, largura, altura):
        painel = pygame.Surface((largura, altura), pygame.SRCALPHA)
        painel.fill(CINZA_TRANSPARENTE)
        pygame.draw.rect(painel, VERDE_MATRIX, painel.get_rect(), 2)
        superficie.blit(painel, (x, y))

        titulo = FONTE_TITULO.render("🏆 PLACAR GLOBAL 🏆", True, AMARELO)
        superficie.blit(titulo, (x + (largura - titulo.get_width()) // 2, y + 15))

        # Cabeçalho
        txt_pos = FONTE_SUBTITULO.render("POS", True, VERDE_MATRIX)
        txt_nome = FONTE_SUBTITULO.render("NOME", True, VERDE_MATRIX)
        txt_pts = FONTE_SUBTITULO.render("PONTOS", True, VERDE_MATRIX)
        superficie.blit(txt_pos, (x + 25, y + 55))
        superficie.blit(txt_nome, (x + 90, y + 55))
        superficie.blit(txt_pts, (x + 260, y + 55))

        pygame.draw.line(superficie, VERDE_ESCURO, (x + 15, y + 85), (x + largura - 15, y + 85), 2)

        if not self.pontuacoes:
            sem_dados = FONTE_TEXTO.render("Nenhuma pontuação salva.", True, BRANCO)
            superficie.blit(sem_dados, (x + (largura - sem_dados.get_width()) // 2, y + 120))
        else:
            for idx, item in enumerate(self.pontuacoes[:8]):
                offset_y = y + 95 + (idx * 26)
                cor = AMARELO if idx == 0 else (BRANCO if idx < 3 else (180, 180, 180))
                
                pos_str = f"#{idx+1}"
                nome_str = str(item['nome'])[:12]
                pts_str = f"{item['pontos']} pts"

                lbl_pos = FONTE_TEXTO.render(pos_str, True, cor)
                lbl_nome = FONTE_TEXTO.render(nome_str, True, cor)
                lbl_pts = FONTE_TEXTO.render(pts_str, True, cor)

                superficie.blit(lbl_pos, (x + 25, offset_y))
                superficie.blit(lbl_nome, (x + 90, offset_y))
                superficie.blit(lbl_pts, (x + 260, offset_y))


# ==========================================
# GERENCIADOR DO JOGO (ESTADOS)
# ==========================================
class JogoHardware:
    def __init__(self):
        self.fundo = FundoBinario(LARGURA, ALTURA)
        self.placar = PlacarGlobal()
        
        self.estado = "NOME"  # NOME, QUIZ, ENCAIXE, BOOT, GAME_OVER, VITORIA
        self.nome_jogador = ""
        self.pontos = 0
        
        # Controle do Quiz
        self.idx_pergunta = 0
        self.vidas = 2
        
        # Controle do Encaixe
        self.idx_encaixe = 0
        self.opcoes_alvo = []
        self.erros_encaixe = []
        
        # Controle da Tela de Boot
        self.boot_logs = []
        self.boot_timer = 0
        self.boot_step = 0

    def reiniciar(self):
        self.estado = "NOME"
        self.nome_jogador = ""
        self.pontos = 0
        self.idx_pergunta = 0
        self.vidas = 2
        self.idx_encaixe = 0
        self.erros_encaixe = []
        self.boot_logs = []
        self.boot_step = 0

    def preparar_fase_encaixe(self):
        self.estado = "ENCAIXE"
        todos_alvos = [item["alvo"] for item in ENCAIXE_DATA]
        random.shuffle(todos_alvos)
        self.opcoes_alvo = todos_alvos

    def processar_eventos(self, evento):
        # 1. TELA DE INSERIR NOME
        if self.estado == "NOME":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and self.nome_jogador.strip():
                    self.estado = "QUIZ"
                elif evento.key == pygame.K_BACKSPACE:
                    self.nome_jogador = self.nome_jogador[:-1]
                else:
                    if len(self.nome_jogador) < 12 and (evento.unicode.isalnum() or evento.unicode in [" ", "_", "-"]):
                        self.nome_jogador += evento.unicode

        # 2. TELA DO QUIZ (8 PERGUNTAS)
        elif self.estado == "QUIZ":
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    opcao_escolhida = evento.key - pygame.K_1
                    q = QUIZ_DATA[self.idx_pergunta]
                    
                    if opcao_escolhida == q["correta"]:
                        self.pontos += 100
                    else:
                        self.vidas -= 1

                    self.idx_pergunta += 1

                    if self.vidas <= 0:
                        self.erros_encaixe.append("Você esgotou todas as suas vidas no Quiz de Hardware.")
                        self.placar.adicionar_pontuacao(self.nome_jogador, self.pontos)
                        self.estado = "GAME_OVER"
                    elif self.idx_pergunta >= len(QUIZ_DATA):
                        self.preparar_fase_encaixe()

        # 3. TELA DE ENCAIXE DE PEÇAS (5 PEÇAS)
        elif self.estado == "ENCAIXE":
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    idx_alvo = evento.key - pygame.K_1
                    if idx_alvo < len(self.opcoes_alvo):
                        alvo_selecionado = self.opcoes_alvo[idx_alvo]
                        peca_atual = ENCAIXE_DATA[self.idx_encaixe]

                        if alvo_selecionado == peca_atual["alvo"]:
                            self.pontos += 150
                        else:
                            self.erros_encaixe.append(
                                f"A peça '{peca_atual['nome']}' foi colocada incorretamente em '{alvo_selecionado}'.\n"
                                f"MOTIVO: {peca_atual['motivo']}"
                            )

                        self.idx_encaixe += 1

                        if self.idx_encaixe < len(ENCAIXE_DATA):
                            todos_alvos = [item["alvo"] for item in ENCAIXE_DATA]
                            random.shuffle(todos_alvos)
                            self.opcoes_alvo = todos_alvos
                        else:
                            if len(self.erros_encaixe) > 0:
                                self.placar.adicionar_pontuacao(self.nome_jogador, self.pontos)
                                self.estado = "GAME_OVER"
                            else:
                                self.estado = "BOOT"
                                self.boot_timer = pygame.time.get_ticks()

        # 4. TELA FINAL / GAME OVER / VITORIA
        elif self.estado in ["GAME_OVER", "VITORIA"]:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.reiniciar()

    def desenhar(self, superficie):
        self.fundo.desenhar_e_atualizar(superficie)

        # 1. TELA NOME + PLACAR GLOBAL VISÍVEL AO LADO
        if self.estado == "NOME":
            # Painel do Jogador
            painel = pygame.Surface((420, 360), pygame.SRCALPHA)
            painel.fill(CINZA_TRANSPARENTE)
            pygame.draw.rect(painel, VERDE_MATRIX, painel.get_rect(), 2)
            superficie.blit(painel, (40, 150))

            txt = FONTE_TITULO.render("HARDWARE MASTER", True, AMARELO)
            lbl = FONTE_SUBTITULO.render("Digite seu nome para iniciar:", True, BRANCO)
            nome_txt = FONTE_TITULO.render(f"> {self.nome_jogador}_", True, VERDE_MATRIX)
            dica = FONTE_TEXTO.render("Pressione [ENTER] para começar", True, BRANCO)

            superficie.blit(txt, (40 + (420 - txt.get_width()) // 2, 180))
            superficie.blit(lbl, (60, 240))
            superficie.blit(nome_txt, (60, 280))
            superficie.blit(dica, (60, 390))

            # PLACAR GLOBAL EXIBIDO NO MENU
            self.placar.desenhar(superficie, x=490, y=150, largura=420, altura=360)

        # 2. TELA QUIZ
        elif self.estado == "QUIZ":
            q = QUIZ_DATA[self.idx_pergunta]

            painel = pygame.Surface((800, 500), pygame.SRCALPHA)
            painel.fill(CINZA_TRANSPARENTE)
            pygame.draw.rect(painel, VERDE_MATRIX, painel.get_rect(), 2)
            superficie.blit(painel, (75, 75))

            info = FONTE_TEXTO.render(f"Jogador: {self.nome_jogador} | Pts: {self.pontos} | Vidas: {'❤️'*self.vidas}", True, AMARELO)
            prog = FONTE_SUBTITULO.render(f"Pergunta {self.idx_pergunta + 1} de {len(QUIZ_DATA)}", True, VERDE_MATRIX)
            perg = FONTE_SUBTITULO.render(q["pergunta"], True, BRANCO)

            superficie.blit(info, (95, 95))
            superficie.blit(prog, (95, 125))
            superficie.blit(perg, (95, 165))

            for idx, op in enumerate(q["opcoes"]):
                btn_txt = FONTE_TEXTO.render(f"[{idx+1}]  {op}", True, AZUL_CLARO)
                superficie.blit(btn_txt, (110, 230 + (idx * 50)))

            dica = FONTE_MINI.render("Digite o número (1, 2, 3 ou 4) no teclado", True, BRANCO)
            superficie.blit(dica, (95, 500))

        # 3. TELA ENCAIXE DE PEÇAS
        elif self.estado == "ENCAIXE":
            peca = ENCAIXE_DATA[self.idx_encaixe]

            painel = pygame.Surface((800, 500), pygame.SRCALPHA)
            painel.fill(CINZA_TRANSPARENTE)
            pygame.draw.rect(painel, AZUL_CLARO, painel.get_rect(), 2)
            superficie.blit(painel, (75, 75))

            titulo = FONTE_TITULO.render("🛠️ ETAPA DE MONTAGEM DE HARDWARE", True, AMARELO)
            inst = FONTE_TEXTO.render(f"Onde deve ser encaixada a peça [{self.idx_encaixe+1}/5] abaixo?", True, BRANCO)
            peca_txt = FONTE_SUBTITULO.render(f"PEÇA ATUAL: {peca['nome']}", True, VERDE_MATRIX)

            superficie.blit(titulo, (95, 90))
            superficie.blit(inst, (95, 130))
            superficie.blit(peca_txt, (95, 160))

            for idx, alvo in enumerate(self.opcoes_alvo):
                slot_txt = FONTE_TEXTO.render(f"[{idx+1}] Slot/Conector: {alvo}", True, BRANCO)
                superficie.blit(slot_txt, (110, 220 + (idx * 45)))

            dica = FONTE_MINI.render("Digite o número do Slot de encaixe correto (1 a 5)!", True, AMARELO)
            superficie.blit(dica, (95, 500))

        # 4. TELA BOOT
        elif self.estado == "BOOT":
            painel = pygame.Surface((800, 500), pygame.SRCALPHA)
            painel.fill((0, 5, 0, 240))
            pygame.draw.rect(painel, VERDE_MATRIX, painel.get_rect(), 2)
            superficie.blit(painel, (75, 75))

            logs_disponiveis = [
                "[0.01s] BIOS/UEFI Check... OK",
                "[0.15s] Energizando barramentos da Placa-Mãe...",
                "[0.35s] Checando Soquete da CPU & Instruções x86... OK",
                "[0.60s] Testando canais de Memória RAM Dual-Channel... OK",
                "[0.85s] Inicializando GPU PCIe x16 e exibição de vídeo... OK",
                "[1.10s] Lendo taxas de transferência do SSD M.2 NVMe... OK",
                "[1.40s] Sistema Operacional Carregado com Sucesso!",
                "---------------------------------------------------",
                "COMPUTADOR LIGADO E FUNCIONANDO 100%!"
            ]

            agora = pygame.time.get_ticks()
            if agora - self.boot_timer > 350 and self.boot_step < len(logs_disponiveis):
                self.boot_logs.append(logs_disponiveis[self.boot_step])
                self.boot_step += 1
                self.boot_timer = agora

            for idx, log in enumerate(self.boot_logs):
                cor = AMARELO if idx == len(logs_disponiveis) - 1 else VERDE_MATRIX
                log_txt = FONTE_MINI.render(log, True, cor)
                superficie.blit(log_txt, (95, 95 + (idx * 30)))

            if self.boot_step >= len(logs_disponiveis):
                if agora - self.boot_timer > 1500:
                    self.placar.adicionar_pontuacao(self.nome_jogador, self.pontos)
                    self.estado = "VITORIA"

        # 5. TELA DE ERRO / GAME OVER COM MOTIVOS
        elif self.estado == "GAME_OVER":
            painel = pygame.Surface((840, 540), pygame.SRCALPHA)
            painel.fill(CINZA_TRANSPARENTE)
            pygame.draw.rect(painel, VERMELHO, painel.get_rect(), 2)
            superficie.blit(painel, (55, 50))

            tit = FONTE_TITULO.render("💥 O COMPUTADOR NÃO LIGOU!", True, VERMELHO)
            sub = FONTE_SUBTITULO.render("Falha crítica de montagem/conhecimento:", True, BRANCO)
            superficie.blit(tit, (75, 70))
            superficie.blit(sub, (75, 105))

            y_err = 140
            for err in self.erros_encaixe:
                linhas = err.split("\n")
                for l in linhas:
                    err_txt = FONTE_MINI.render(l, True, AMARELO if "MOTIVO" in l else BRANCO)
                    superficie.blit(err_txt, (75, y_err))
                    y_err += 22
                y_err += 10

            btn = FONTE_SUBTITULO.render("Pressione [ENTER] para reiniciar o jogo", True, VERDE_MATRIX)
            superficie.blit(btn, (75, 535))

        # 6. TELA DE VITÓRIA COM PLACAR GLOBAL DESTACADO
        elif self.estado == "VITORIA":
            painel_txt = FONTE_TITULO.render("🎉 PARABÉNS! MONTAGEM E BOOT CONCLUÍDOS!", True, VERDE_MATRIX)
            pts_txt = FONTE_SUBTITULO.render(f"Jogador: {self.nome_jogador} | Pontuação Final: {self.pontos} Pts", True, AMARELO)
            
            superficie.blit(painel_txt, ((LARGURA - painel_txt.get_width()) // 2, 40))
            superficie.blit(pts_txt, ((LARGURA - pts_txt.get_width()) // 2, 80))

            # Placar Global Centralizado na Tela de Vitória
            self.placar.desenhar(superficie, x=225, y=120, largura=500, altura=420)

            rst_txt = FONTE_SUBTITULO.render("Pressione [ENTER] para jogar novamente", True, BRANCO)
            superficie.blit(rst_txt, ((LARGURA - rst_txt.get_width()) // 2, 580))


# ==========================================
# LOOP PRINCIPAL DO PROGRAMA
# ==========================================
def main():
    jogo = JogoHardware()
    rodando = True

    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False
            else:
                jogo.processar_eventos(evento)

        jogo.desenhar(tela)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
