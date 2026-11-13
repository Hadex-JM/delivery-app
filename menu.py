from delivery import (Bebida, Cliente, Entregador, Pedido, Prato, Restaurante, Sobremesa,
                      StatusPedido)


class Menu:
    def __init__(self, restaurante: Restaurante):
        self.restaurante = restaurante

    @staticmethod
    def ler_texto(mensagem: str) -> str:
        while True:
            texto = input(mensagem).strip()
            if texto:
                return texto
            print("  Campo obrigatório.")

    @staticmethod
    def ler_inteiro(mensagem: str, minimo: int | None = None) -> int:
        while True:
            try:
                valor = int(input(mensagem).strip())
            except ValueError:
                print("  Digite um número inteiro.")
                continue
            if minimo is not None and valor < minimo:
                print(f"  Digite um número a partir de {minimo}.")
                continue
            return valor

    @staticmethod
    def ler_decimal(mensagem: str) -> float:
        while True:
            try:
                return float(input(mensagem).strip().replace(",", "."))
            except ValueError:
                print("  Digite um número. Exemplo: 25,90")

    @staticmethod
    def ler_sim_nao(mensagem: str) -> bool:
        while True:
            resposta = input(f"{mensagem} (s/n): ").strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("  Responda s ou n.")

    @staticmethod
    def pausar() -> None:
        input("\nAperte Enter para continuar...")

    def escolher_da_lista(self, titulo: str, itens: list, vazio: str = "A lista está vazia."):
        if not itens:
            raise ValueError(vazio)
        print(f"\n{titulo}")
        for i, item in enumerate(itens, start=1):
            print(f"  {i}. {item}")
        while True:
            numero = self.ler_inteiro("Escolha o número: ", 1)
            if numero <= len(itens):
                return itens[numero - 1]
            print(f"  Escolha entre 1 e {len(itens)}.")

    def escolher_cliente(self) -> Cliente:
        return self.escolher_da_lista("Clientes", self.restaurante.clientes,
                                      "Nenhum cliente cadastrado.")

    def escolher_entregador(self, so_disponiveis: bool = False) -> Entregador:
        lista = (self.restaurante.entregadores_disponiveis() if so_disponiveis
                 else self.restaurante.entregadores)
        vazio = "Nenhum entregador disponível." if so_disponiveis else "Nenhum entregador cadastrado."
        return self.escolher_da_lista("Entregadores", lista, vazio)

    def escolher_pedido(self, titulo: str, pedidos: list[Pedido], vazio: str) -> Pedido:
        return self.escolher_da_lista(titulo, pedidos, vazio)

    def mostrar_cardapio(self, so_disponiveis: bool = True) -> None:
        produtos = self.restaurante.cardapio(so_disponiveis)
        print(f"\nCARDÁPIO - {self.restaurante.nome}")
        if not produtos:
            print("  (vazio)")
        for produto in produtos:
            print(f"  {produto}")

    def executar_menu(self, titulo: str, opcoes: list[tuple[str, callable]],
                      texto_sair: str = "Voltar", submenus: tuple = ()) -> None:
        while True:
            print(f"\n{'=' * 50}\n{titulo}\n{'=' * 50}")
            for numero, (texto, _) in enumerate(opcoes, start=1):
                print(f"  {numero}. {texto}")
            print(f"  0. {texto_sair}")
            escolha = input("Opção: ").strip()
            if escolha == "0":
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(opcoes):
                print("  Opção inválida.")
                continue
            texto, acao = opcoes[int(escolha) - 1]
            if acao in submenus:
                acao()
                continue
            print(f"\n--- {texto} ---")
            try:
                acao()
            except ValueError as erro:
                print(f"\n  Não foi possível: {erro}")
            self.pausar()

    def executar(self) -> None:
        self.executar_menu(f"APP DE DELIVERY - {self.restaurante.nome}", [
            ("Área do cliente", self.menu_cliente),
            ("Área do atendente", self.menu_atendente),
            ("Área do entregador", self.menu_entregador),
            ("Carregar dados de exemplo", self.carregar_exemplo),
        ], texto_sair="Sair",
            submenus=(self.menu_cliente, self.menu_atendente, self.menu_entregador))
        print("Até logo!")

    def menu_cliente(self) -> None:
        self.executar_menu("ÁREA DO CLIENTE", [
            ("Cadastrar cliente", self.cadastrar_cliente),
            ("Ver cardápio", self.ver_cardapio),
            ("Fazer pedido", self.fazer_pedido),
            ("Acompanhar meus pedidos", self.acompanhar_pedidos),
            ("Cancelar pedido", self.cancelar_pedido),
        ])

    def cadastrar_cliente(self) -> None:
        cliente = Cliente(
            self.ler_texto("Nome: "),
            self.ler_texto("CPF (só números): "),
            self.ler_texto("Telefone (só números): "),
            self.ler_texto("Endereço: "),
            self.ler_decimal("Distância até o restaurante (km): "),
        )
        self.restaurante.cadastrar_cliente(cliente)
        print(f"\n  Cadastrado: {cliente}")

    def ver_cardapio(self) -> None:
        categoria = input("Filtrar por categoria (prato, bebida, sobremesa) ou Enter para todas: ").strip()
        if not categoria:
            self.mostrar_cardapio()
            return
        produtos = self.restaurante.listar_por_categoria(categoria)
        print(f"\n{categoria.upper()}")
        if not produtos:
            print("  Nenhum produto nessa categoria.")
        for produto in produtos:
            print(f"  {produto}")

    def fazer_pedido(self) -> None:
        cliente = self.escolher_cliente()
        if not self.restaurante.cardapio():
            raise ValueError("O cardápio está vazio.")
        pedido = self.restaurante.novo_pedido(cliente)
        print(f"\n  Pedido #{pedido.numero} aberto para {cliente.nome}.")
        while True:
            print("\n  1. Adicionar item   2. Remover item   3. Ver pedido   4. Finalizar   0. Desistir")
            escolha = input("  Opção: ").strip()
            try:
                if escolha == "1":
                    self.mostrar_cardapio()
                    codigo = self.ler_inteiro("Código do produto: ")
                    quantidade = self.ler_inteiro("Quantidade: ", 1)
                    self.restaurante.adicionar_ao_pedido(pedido, codigo, quantidade)
                    print(f"  Adicionado. Subtotal: R$ {pedido.subtotal():.2f}")
                elif escolha == "2":
                    print(pedido.resumo())
                    codigo = self.ler_inteiro("Código do produto para remover: ")
                    self.restaurante.remover_do_pedido(pedido, codigo)
                    print("  Removido.")
                elif escolha == "3":
                    print(pedido.resumo())
                elif escolha == "4":
                    self.restaurante.finalizar_pedido(pedido)
                    print("\n  Pedido enviado ao restaurante!")
                    print(pedido.resumo())
                    return
                elif escolha == "0":
                    self.restaurante.cancelar_pedido(pedido)
                    print(f"  Pedido #{pedido.numero} cancelado.")
                    return
                else:
                    print("  Opção inválida.")
            except ValueError as erro:
                print(f"  Não foi possível: {erro}")

    def acompanhar_pedidos(self) -> None:
        cliente = self.escolher_cliente()
        if not cliente.pedidos:
            print(f"\n  {cliente.nome} ainda não fez pedidos.")
            return
        for pedido in cliente.pedidos:
            print()
            print(pedido.resumo())

    def cancelar_pedido(self) -> None:
        cliente = self.escolher_cliente()
        pedidos = [p for p in cliente.pedidos if p.status in Pedido.PODE_CANCELAR]
        pedido = self.escolher_pedido("Pedidos que ainda podem ser cancelados", pedidos,
                                      f"{cliente.nome} não tem pedidos que possam ser cancelados.")
        self.restaurante.cancelar_pedido(pedido)
        print(f"\n  {pedido}")

    def menu_atendente(self) -> None:
        self.executar_menu("ÁREA DO ATENDENTE", [
            ("Cadastrar produto", self.cadastrar_produto),
            ("Ver cardápio completo", lambda: self.mostrar_cardapio(so_disponiveis=False)),
            ("Alterar preço", self.alterar_preco),
            ("Marcar produto disponível / indisponível", self.mudar_disponibilidade),
            ("Cadastrar entregador", self.cadastrar_entregador),
            ("Listar clientes e entregadores", self.listar_pessoas),
            ("Buscar cliente por CPF", self.buscar_cliente),
            ("Ver pedidos", self.ver_pedidos),
            ("Iniciar preparo de pedido", self.iniciar_preparo),
            ("Enviar pedido para entrega", self.enviar_pedido),
            ("Ver faturamento", self.ver_faturamento),
        ])

    def cadastrar_produto(self) -> None:
        tipo = self.escolher_da_lista("Tipo de produto", ["Prato", "Bebida", "Sobremesa"])
        nome = self.ler_texto("Nome: ")
        preco = self.ler_decimal("Preço (R$): ")
        if tipo == "Prato":
            produto = Prato(nome, preco, self.ler_inteiro("Serve quantas pessoas: ", 1))
        elif tipo == "Bebida":
            produto = Bebida(nome, preco, self.ler_inteiro("Volume (ml): ", 1))
        else:
            produto = Sobremesa(nome, preco, self.ler_sim_nao("É gelada?"))
        self.restaurante.cadastrar_produto(produto)
        print(f"\n  Cadastrado: {produto}")

    def alterar_preco(self) -> None:
        self.mostrar_cardapio(so_disponiveis=False)
        codigo = self.ler_inteiro("Código do produto: ")
        produto = self.restaurante.buscar_produto(codigo)
        print(f"  Preço atual: R$ {produto.preco:.2f}")
        self.restaurante.alterar_preco(codigo, self.ler_decimal("Novo preço (R$): "))
        print(f"\n  Atualizado: {produto}")

    def mudar_disponibilidade(self) -> None:
        self.mostrar_cardapio(so_disponiveis=False)
        codigo = self.ler_inteiro("Código do produto: ")
        produto = self.restaurante.buscar_produto(codigo)
        if produto.disponivel:
            self.restaurante.marcar_indisponivel(codigo)
        else:
            self.restaurante.marcar_disponivel(codigo)
        print(f"\n  Atualizado: {produto}")

    def cadastrar_entregador(self) -> None:
        entregador = Entregador(
            self.ler_texto("Nome: "),
            self.ler_texto("CPF (só números): "),
            self.ler_texto("Telefone (só números): "),
            self.ler_texto("Veículo: "),
        )
        self.restaurante.cadastrar_entregador(entregador)
        print(f"\n  Cadastrado: {entregador}")

    def listar_pessoas(self) -> None:
        print("\nCLIENTES")
        for cliente in self.restaurante.clientes or ["(nenhum)"]:
            print(f"  {cliente}")
        print("\nENTREGADORES")
        for entregador in self.restaurante.entregadores or ["(nenhum)"]:
            print(f"  {entregador}")

    def buscar_cliente(self) -> None:
        cliente = self.restaurante.buscar_cliente(self.ler_texto("CPF: "))
        if cliente is None:
            raise ValueError("Cliente não encontrado.")
        print(f"\n  {cliente}")
        print(f"  Telefone: {cliente.telefone} | Pedidos feitos: {len(cliente.pedidos)}")

    def ver_pedidos(self) -> None:
        opcoes = ["Todos"] + [status.value for status in StatusPedido]
        escolha = self.escolher_da_lista("Filtrar por situação", opcoes)
        if escolha == "Todos":
            pedidos = self.restaurante.pedidos
        else:
            pedidos = self.restaurante.pedidos_por_status(StatusPedido(escolha))
        print()
        if not pedidos:
            print("  Nenhum pedido.")
        for pedido in pedidos:
            print(f"  {pedido}")

    def iniciar_preparo(self) -> None:
        pedidos = self.restaurante.pedidos_por_status(StatusPedido.AGUARDANDO)
        pedido = self.escolher_pedido("Pedidos aguardando", pedidos, "Nenhum pedido aguardando preparo.")
        self.restaurante.iniciar_preparo(pedido)
        print(f"\n  {pedido}")

    def enviar_pedido(self) -> None:
        pedidos = self.restaurante.pedidos_por_status(StatusPedido.EM_PREPARO)
        pedido = self.escolher_pedido("Pedidos em preparo", pedidos, "Nenhum pedido em preparo.")
        if self.ler_sim_nao("Escolher o entregador? (n = primeiro disponível)"):
            entregador = self.restaurante.enviar_pedido(pedido, self.escolher_entregador(so_disponiveis=True))
        else:
            entregador = self.restaurante.enviar_pedido(pedido)
        print(f"\n  {pedido}")
        print(f"  {entregador}")

    def ver_faturamento(self) -> None:
        entregues = self.restaurante.pedidos_por_status(StatusPedido.ENTREGUE)
        print(f"\n  Pedidos entregues: {len(entregues)}")
        print(f"  Faturamento: R$ {self.restaurante.faturamento():.2f}")

    def menu_entregador(self) -> None:
        self.executar_menu("ÁREA DO ENTREGADOR", [
            ("Ver minha entrega", self.ver_minha_entrega),
            ("Confirmar entrega", self.confirmar_entrega),
        ])

    def entregas_de(self, entregador: Entregador) -> list[Pedido]:
        return [p for p in self.restaurante.pedidos_por_status(StatusPedido.A_CAMINHO)
                if p.entregador is entregador]

    def ver_minha_entrega(self) -> None:
        entregador = self.escolher_entregador()
        entregas = self.entregas_de(entregador)
        if not entregas:
            print(f"\n  {entregador.nome} não tem entregas no momento.")
            return
        for pedido in entregas:
            print()
            print(pedido.resumo())
            print(f"  Endereço: {pedido.cliente.endereco} ({pedido.cliente.distancia_km} km)")

    def confirmar_entrega(self) -> None:
        entregador = self.escolher_entregador()
        pedido = self.escolher_pedido("Minhas entregas", self.entregas_de(entregador),
                                      f"{entregador.nome} não tem entregas no momento.")
        self.restaurante.confirmar_entrega(pedido)
        print(f"\n  {pedido}")
        print(f"  {entregador}")

    def carregar_exemplo(self) -> None:
        if self.restaurante.cardapio(so_disponiveis=False) or self.restaurante.clientes:
            raise ValueError("Já existem dados cadastrados.")
        for produto in (Prato("Lasanha", 30.0, 2), Prato("Strogonoff", 25.0, 1),
                        Bebida("Suco de laranja", 8.0, 500), Bebida("Refrigerante", 6.0, 350),
                        Sobremesa("Pudim", 10.0), Sobremesa("Sorvete", 12.0, gelada=True)):
            self.restaurante.cadastrar_produto(produto)
        self.restaurante.cadastrar_cliente(
            Cliente("Ana Souza", "12345678901", "61999990000", "Rua das Flores, 10", 4.0))
        self.restaurante.cadastrar_cliente(
            Cliente("Bruno Lima", "98765432100", "61988880000", "Av. Central, 200", 10.0))
        self.restaurante.cadastrar_entregador(
            Entregador("João Pedro", "11122233344", "61977770000", "moto"))
        self.restaurante.cadastrar_entregador(
            Entregador("Leo Alves", "55566677788", "61966660000", "bicicleta"))
        print("  Carregados: 6 produtos, 2 clientes e 2 entregadores.")
        self.listar_pessoas()
        self.mostrar_cardapio()


if __name__ == "__main__":
    try:
        Menu(Restaurante("Sabor Express")).executar()
    except (KeyboardInterrupt, EOFError):
        print("\nAté logo!")