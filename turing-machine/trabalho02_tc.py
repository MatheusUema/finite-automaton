# -*- coding: utf-8 -*-
"""Trabalho02-TC.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dsynIh1Vd4WCu78HdH74AZc97Z1N3riC
"""

# Acessando informações do arquivo
arquivo = open("entrada.txt", "r")
linha = arquivo.readline()
linhas = []
while linha != "":
    linhas.append(linha)
    linha = arquivo.readline()
arquivo.close()


print(linhas)

# Atribuindo informações para autômato finito
def get_info(linha):
  return linha.replace('\n', '')

class State:
  def __init__(self, state):
    self.state = state
    self.is_initial = False
    self.is_acceptance = False
    self.transitions = []

  def set_as_initial(self):
    self.is_initial = True

  def set_as_acceptance(self):
    self.is_acceptance = True;

  def add_transition(self, transition):
    self.transitions.append(transition)

  def get_transition(self, chain, chain_position, terminal):
    next_state = None
    new_chain = chain
    current_chain_position = chain_position
    for transition in self.transitions:
      if transition.terminal == terminal:
        next_state = transition.next_state
        new_chain = chain[: chain_position] + transition.substitute + chain[chain_position + 1:]
        current_chain_position = chain_position + self.get_direction(transition.direction)
        break
    return next_state, new_chain, current_chain_position

  def get_direction(self, direction):
    if direction == 'R':
      return +1
    elif direction == 'L':
      return -1
    return 0

class Transition:
  def __init__(self, transition):
    transition_info = transition.split(' ')
    self.current_state = int(transition_info[0])
    self.terminal = transition_info[1]
    self.next_state = int(transition_info[2])
    self.substitute = transition_info[3]
    self.direction = transition_info[4]

class Turing_Machine:
  def __init__(self, linhas, verbose=True):
    try:
        #Número de estados
        state_number = int(get_info(linhas[0]))
        self.states = []
        for i in range(0, state_number):
          state = State(i)
          self.states.append(state)

        self.states[0].set_as_initial()

        #Terminais
        terminals_info = get_info(linhas[1]).split(' ')
        terminal_quantity = int(terminals_info[0])
        self.terminals = []
        for i in range(1, terminal_quantity+1):
          self.terminals.append(terminals_info[i])

        #Alfabeto Estendido da Fita
        not_terminals_info = get_info(linhas[2]).split(' ')
        not_terminals_quantity = int(not_terminals_info[0])
        self.not_terminals = []
        for i in range(1, not_terminals_quantity+1):
          self.not_terminals.append(not_terminals_info[i])

        #Estados de aceitação
        acceptance_info = get_info(linhas[3]).split(' ')
        acceptance_state = int(acceptance_info[0])
        self.acceptance_states = []
        self.states[acceptance_state].set_as_acceptance()
        self.acceptance_states.append(acceptance_state)
        print(self.acceptance_states)

        #Transições
        transitions_amount = int(get_info(linhas[4]))
        current_line = 4
        for i in range(0, transitions_amount):
          current_line += 1
          transition = Transition(get_info(linhas[current_line]))
          state = int(get_info(linhas[current_line]).split(' ')[0])
          self.states[state].add_transition(transition)

        #Cadeias para teste
        current_line += 1
        test_cases_amount = int(get_info(linhas[current_line]))
        self.test_cases = []
        for i in range(0, test_cases_amount):
          current_line += 1
          self.test_cases.append(get_info(linhas[current_line]))

    except:
        print("Arquivo de entrada incorreto")

    self.verbose = verbose
    # Resumo do autômato
    if verbose:
      self.get_summary()

  def generate_output(self):
    #Escrever arquivo de saída
    output = open("saida.txt", "w")

    for chain in self.test_cases:
      result = False
      try:
        result = self.test_chain(chain)
      except:
        "Algum erro occoreu, verifique se as entradas estão corretas"
      if result:
        output.write("aceita\n")
      else:
        output.write("rejeita\n")
    output.close()


  def test_chain(self, chain):
    #Testa cadeia atual
    chain_length = len(chain)

    if self.verbose:
      print("==================")
      print("Iniciando teste para cadeia:", chain)
      print("Estado inicial:", self.states[0].state)

    resultado = self.test_current_terminal("B" + chain + "B", 1, self.states[0])

    if self.verbose:
      print("Resultado:", resultado)
    return resultado

  def test_current_terminal(self, chain, position, current_state):
    current_terminal = self.get_character(chain, position)
    next_state, new_chain, new_position = current_state.get_transition(chain, position, current_terminal)

    if next_state is None:
      return False
    if self.states[next_state].is_acceptance:
      return True

    if self.verbose:
      print("delta(" + str(current_state.state) + ", " + str(current_terminal) + ") =", next_state)
      print("old chain:", chain[: position] + "->" + chain[position:])
      print("new_chain:", new_chain[: new_position] + "->" + new_chain[new_position:])
      print("\n")

    return self.test_current_terminal(new_chain, new_position, self.states[next_state])

  def get_character(self, chain, position):
    return chain[position]

  def get_summary(self):
    print("Terminais: " + ', '.join(self.terminals))
    print("Não Terminais: " + ', '.join(self.not_terminals))
    print("Estado iniciail: " + '[' + str(self.states[0].state) + ']')
    print("Estado de aceitação: " + '[' +  ', '.join(str(acceptance_state) for acceptance_state in self.acceptance_states) + ']')
    print("Número de estados: " + str(len(self.states)))
    for i in range(0, len(self.states)):
      if i not in self.acceptance_states:
        print(" Transições do Estado " + str(self.states[i].state) +":")
        for j in range(0, len(self.states[i].transitions)):
          print("   delta(" + str(self.states[i].transitions[j].current_state) + ", " + self.states[i].transitions[j].terminal + ") = " + "(" + str(self.states[i].transitions[j].next_state) + ", " + str(self.states[i].transitions[j].substitute) + ", " + str(self.states[i].transitions[j].direction) + ")")

automaton = Turing_Machine(linhas, verbose=True)
automaton.generate_output()