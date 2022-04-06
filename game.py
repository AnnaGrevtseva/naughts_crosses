import sys
import typer
import painter as pnt
import game_manager as gm
import pickle


def main(n: int = typer.Option(..., help="Number of field rows", min=1, max=40),
         k: int = typer.Option(..., help="Number of field columns", min=1, max=40),
         symbol: gm.Symbols = typer.Option(gm.Symbols.X, help="User's symbol"),
         inputFilePath: str = typer.Option(None, help="Input file path"),
         outputFilePath: str = typer.Option(None, help="Output file path")):

    typer.echo(f"Field size: {n}, {k}")

    painter = pnt.Painter(n, k)

    gameManager = gm.GameManager(n, k, symbol.value)

    if inputFilePath is not None:
        with open(inputFilePath, 'rb') as file:
            field = pickle.load(file)
            gameManager.setField(field)
            painter.paint(gameManager.getField())

    while not gameManager.finished():
        while True:
            print("Enter the step coordinates (or 's' to save, or 'q' to quit):")
            inputValue = input().split()
            inputSave = False
            inputQuit = False
            inputRow = None
            inputCol = None

            try:
                if 1 == len(inputValue) and 's' == inputValue[0]:
                    inputSave = True
                elif 1 == len(inputValue) and 'q' == inputValue[0]:
                    inputQuit = True
                elif 2 == len(inputValue):
                    inputRow = int(inputValue[0])
                    inputCol = int(inputValue[1])

                    if inputRow >= n or inputCol >= k:
                        print(f"Coordinate values must be less than size field: x < {n}, y < {k}!")
                        raise ValueError
                    elif gameManager.isAlreadySet((inputRow, inputCol)):
                        print(f"Point with coordinates ({inputRow}, {inputCol}) is already set!")
                        raise ValueError

                else:
                    raise ValueError

            except ValueError:
                print("Invalid input arguments!")

            else:
                if inputSave:
                    outputFilePath = 'save_game.dat' if outputFilePath is None else outputFilePath
                    with open('save_game.dat', 'wb') as file:
                        pickle.dump(gameManager.getField(), file)

                elif inputQuit:
                    sys.exit()

                elif inputRow is not None and inputCol is not None:
                    gameManager.step((inputRow, inputCol))
                    painter.paint(gameManager.getField())

                break


if __name__ == "__main__":
    typer.run(main)


