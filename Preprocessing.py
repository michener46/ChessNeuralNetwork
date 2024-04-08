
import json

def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)

def fen_to_board_array(fen):
    piece_encoding = {
        'p': 1, 'P': 2,
        'n': 3, 'N': 4,
        'b': 5, 'B': 6,
        'r': 7, 'R': 8,
        'q': 9, 'Q': 10,
        'k': 11, 'K': 12
    }
    board = []
    for char in fen:
        if char.isdigit():
            board.extend([0] * int(char))
        elif char in piece_encoding:
            board.append(piece_encoding[char])
        elif char == '/':
            continue
        else:
            raise ValueError(f"Unexpected character in FEN string: {char}")
    if len(board) != 64:
        raise ValueError("Processed board does not contain 64 squares")
    return board

# Assuming the file 'lichess_db_eval.jsonl' is in the current directory.
input_file_path = 'lichess_db_eval.jsonl'
output_file_path = 'lichess_db_eval_modified.jsonl'

total_lines = count_lines(input_file_path)
processed_lines = 0

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        data = json.loads(line)
        if 'fen' in data:
            board_array = fen_to_board_array(data['fen'].split()[0])  # Only take the board part of the FEN string
            data['board_position'] = board_array
        output_file.write(json.dumps(data) + '\n')
        processed_lines += 1
        if processed_lines % 1000 == 0:  # Update the progress every 1000 lines to reduce the amount of printing.
            percentage = (processed_lines / total_lines) * 100
            print(f"Processing: {processed_lines}/{total_lines} lines ({percentage:.2f}%)")

print("Processing complete. The modified data has been saved to 'lichess_db_eval_modified.jsonl'.")
