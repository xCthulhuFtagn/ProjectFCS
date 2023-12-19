import pickle
import numpy as np
from evmdasm import EvmBytecode

with open("model.pkl", "rb") as f:
    model = pickle.load() # yours model
tr = 0.6 # yours threshold
trfrm = lambda string_opcode: np.apply(lambda opcode: string_opcode.count(opcode),opcodes) # yours vectorizer

opcodes = np.array(['STOP', 'ADD', 'MUL', 'SUB','DIV','SDIV', 'MOD', 'SMOD',
    'ADDMOD', 'MULMOD', 'EXP', 'SIGNEXTEND', 'LT', 'GT', 'SLT', 'SGT',
    'EQ', 'ISZERO', 'AND', 'OR', # 'EVMOR'
    'XOR', 'NOT', 'BYTE', 'SHL', 'SHR', 'SAR', 'SHA3', 'ADDRESS', 'BALANCE', 'ORIGIN', 'CALLER', 'CALLVALUE',
    'CALLDATALOAD', 'CALLDATASIZE', 'CALLDATACOPY', 'CODESIZE', 'CODECOPY', 'GASPRICE', 'EXTCODESIZE', 'EXTCODECOPY',
    'RETURNDATASIZE', 'RETURNDATACOPY', 'EXTCODEHASH', 'BLOCKHASH', 'COINBASE', 'TIMESTAMP', 'NUMBER', 'DIFFICULTY',
    'GASLIMIT', 'POP', 'MLOAD', 'MSTORE', 'MSTORE8', 'SLOAD', 'SSTORE', 'JUMP', 'JUMPI', 'PC', 'MSIZE', 'GAS', 'JUMPDEST', 
    'PUSH1', 'PUSH2', 'PUSH3', 'PUSH4', 'PUSH5', 'PUSH6', 'PUSH7', 'PUSH8', 'PUSH9', 'PUSH10', 'PUSH11', 'PUSH12', 'PUSH13', 'PUSH14', 'PUSH15',
    'PUSH16', 'PUSH17', 'PUSH18', 'PUSH19', 'PUSH20', 'PUSH21', 'PUSH22', 'PUSH23', 'PUSH24', 'PUSH25', 'PUSH26', 'PUSH27', 'PUSH28', 'PUSH29', 'PUSH30', 
    'PUSH31', 'PUSH32', 'DUP1', 'DUP2', 'DUP3', 'DUP4', 'DUP5', 'DUP6', 'DUP7', 'DUP8', 'DUP9', 'DUP10', 'DUP11', 'DUP12', 'DUP13', 'DUP14', 'DUP15',
    'DUP16', 'SWAP1', 'SWAP2', 'SWAP3', 'SWAP4', 'SWAP5', 'SWAP6', 'SWAP7', 'SWAP8', 'SWAP9', 'SWAP10', 'SWAP11', 'SWAP12', 'SWAP13', 'SWAP14', 'SWAP15',
    'SWAP16', 'LOG0', 'LOG1', 'LOG2', 'LOG3', 'LOG4', 'CREATE', 'CALL', 'CALLCODE', 'RETURN', 'DELEGATECALL', 'CREATE2', 'STATICCALL', 'REVERT', 'INVALID', 'SELFDESTRUCT',
    #   'ff' : 'SUICIDE',
])

def decompile(_bytecode: str):
    """
    Декомпилирует байткод в опкод
    :param _bytecode: байткод контракта из нового блока
    :return: опкоды в виде str
    """
    print('Decompling to opcodes')
    disassembler = EvmBytecode(_bytecode)
    opcode = disassembler.disassemble().as_string
    print('Normalizing opcode')
    opcode_normalized = opcode.replace(' \n', '\n').replace(' ', ' 0x')
    return opcode_normalized.lower()

def inference(_opcode: str):
    """
    Инференс вашей модели
    :param _opcode:
    :return: класс смарт-контракта
    """
    X = vectorizer(_opcode)
    y_proba = model.predict_proba(X) # скор вашей модели
    return int(y_proba > tr)