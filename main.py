from delivery import Bebida, Cliente, Entregador, Prato, Restaurante, Sobremesa

restaurante = Restaurante("Sabor Express")

restaurante.cadastrar_produto(Prato("Lasanha", 30.0, 2))
restaurante.cadastrar_produto(Bebida("Suco de laranja", 8.0, 500))
restaurante.cadastrar_produto(Sobremesa("Pudim", 10.0))
restaurante.cadastrar_produto(Sobremesa("Sorvete", 12.0, gelada=True))
print("CARDÁPIO")
for produto in restaurante.cardapio():
    print(produto)

ana = Cliente("Ana Souza", "12345678901", "61999990000", "Rua A, 10", 4.0)
joao = Entregador("João Pedro", "11122233344", "61977770000", "moto")
restaurante.cadastrar_cliente(ana)
restaurante.cadastrar_entregador(joao)
print("\nPESSOAS")
print(ana)
print(joao)

pedido = restaurante.novo_pedido(ana)
restaurante.adicionar_ao_pedido(pedido, 1)
restaurante.adicionar_ao_pedido(pedido, 2, 2)
restaurante.adicionar_ao_pedido(pedido, 4)

restaurante.finalizar_pedido(pedido)
print("\nPEDIDO FINALIZADO")
print(pedido.resumo())

print("\nANDAMENTO")
restaurante.iniciar_preparo(pedido)
print(pedido)
restaurante.enviar_pedido(pedido)
print(pedido)
print(joao)
restaurante.confirmar_entrega(pedido)
print(pedido)
print(joao)

restaurante.marcar_indisponivel(3)
outro = restaurante.novo_pedido(ana)
restaurante.adicionar_ao_pedido(outro, 2)
restaurante.cancelar_pedido(outro)
print("\nCARDÁPIO SEM O PUDIM")
for produto in restaurante.cardapio():
    print(produto)
print(f"\n{outro}")
print(f"Faturamento: R$ {restaurante.faturamento():.2f}")