from collections import namedtuple

Rule = namedtuple('Rule', ['state', 'symbol', 'new_state', 'write', 'move'])

qACC = 'q_acc'
qREJ = 'q_rej'
qERR = 'q_err'


class RuleDoesNotExistError(Exception):
    pass

class qError(Exception):
    pass


class TuringMachine:
    def __init__(self, rules: [Rule], tape: str):
        self.rules = rules
        self.state = 'q_0'
        self.index = 0
        self.tape = list(tape)

    def run(self) -> None:
        '''
        Runs the turing machine with the given input
        '''
        self.print_tm()

        while self.state not in (qACC, qREJ):
            user_input = input()
            if user_input == '':
                self.step()
                self.print_tm()
            else:
                break

            if self.state == qERR:
                raise qError()

        print('DONE... STATE =', self.state)

    def step(self):
        '''
        Steps through the turing machine when return is pressed
        '''
        rule = self.return_rule()
        self.state = rule.new_state
        self.tape[self.index] = rule.write
        self.index += 1 if rule.move == '>' else -1
        if self.index < 0:
            self.index = 0

    def print_tm(self) -> None:
        '''
        Prints out the tape, head, and current state
        '''
        print(''.join(self.tape) + '*...')
        print(' '*self.index + '^')
        print(' '*self.index + self.state)

    def return_rule(self) -> Rule:
        '''
        Returns a rule that matches the current state and input
        '''
        for rule in self.rules:
            try:
                current_symbol = self.tape[self.index]
            except IndexError:
                self.tape.append('*')
                current_symbol = '*'
            if rule.state == self.state and rule.symbol == current_symbol:
                return rule
        else:
            raise RuleDoesNotExistError(f'Looking for STATE {self.state} and SYMBOL {current_symbol}')


def parse_tml(file_name: str) -> [Rule]:
    '''
    Reads the .tml file and returns a list of Rules
    '''
    rules = []
    symbols = []

    with open(file_name) as f:
        states = [state.strip() for state in f.readline().split('|')][1:]
        for line in f:
            cells = [cell.strip() for cell in line.rstrip().split('|')]
            symbol, cells = cells[0], cells[1:]
            symbols.append(symbol)

            rules.extend(parse_rules(symbol, cells, states))
   
    print_symbols_available(symbols)
    return rules


def parse_rules(symbol: str, cells: [str], states: [str]) -> [Rule]:
    '''
    Creates the rules for each line in the tml file
    Also returns the symbol for that line
    '''
    rules = []
    for index, cell in enumerate(cells):
        cell_contents = cell.split(',', 3)
        if len(cell_contents) == 1:
            rules.append(Rule(states[index], symbol, cell_contents[0], '', ''))
        elif len(cell_contents) == 3:
            new_state, write, move = cell_contents
            rules.append(Rule(states[index], symbol, new_state, write, move))
    return rules


def print_symbols_available(symbols: [str]) -> None:
    if '*' in symbols:
        symbols.remove('*')
    print(f'Symbols available: {", ".join(symbols)}')


def run():
    file_name = input('File name: ')
    rules = parse_tml(file_name)
    input_str = input('Input string: ')

    tm = TuringMachine(rules, input_str)
    tm.run()  


if __name__ == '__main__':
    run()
