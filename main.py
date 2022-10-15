
import json, os


def getConfig() -> dict:
    with open("config.json", "r") as fobj: return json.load(fobj)

def saveSVG(svgText: str, filename: str="plaid-sheet.svg") -> str:
    path = os.path.join("export", filename)
    with open(path, "w+") as fobj: fobj.write(svgText)
    return path

def generateSVG(config: dict) -> str:
    with open(os.path.join("assets", "line_template.svg"), "r") as fobj: line_template = fobj.read()
    with open(os.path.join("assets", "sheet_template.svg"), "r") as fobj: sheet_template = fobj.read()

    horizontal_lines = []
    for i in range(0, config["sheet-height"]):
        posY = i * config["square-size"]
        if posY > config["sheet-height"]: break
        horizontal_lines.append(line_template.format(x1=0, y1=posY, x2=config["sheet-width"], y2=posY, unit=config["unit"]))

    vertical_lines = []
    for i in range(0, config["sheet-width"]):
        posX = i * config["square-size"]
        if posX > config["sheet-width"]: break
        vertical_lines.append(line_template.format(x1=posX, y1=0, x2=posX, y2=config["sheet-height"], unit=config["unit"]))
    
    if config["sheet-cropped"]:
        config["sheet-width"]  = posX - config["square-size"]
        config["sheet-height"] = posY - config["square-size"]

    sheet_svg = sheet_template.format(
        sheet_width    = config["sheet-width"]
        , sheet_height = config["sheet-height"]
        
        , lines_horizontal = "\n".join(horizontal_lines)
        , lines_vertical   = "\n".join(vertical_lines)
        
        , square_size = config["square-size"]
        , sheet_color = config["sheet-color"]
        , line_width  = config["line-width"]
        , line_color  = config["line-color"]
        
        , unit = config["unit"]

        , BO = "{"
        , BC = "}"
    )

    return sheet_svg

def exportSVG(svgFile: str, pngFile: str, scale: int=1) -> int:
    return os.system(f"svgexport {os.path.abspath(svgFile)} {os.path.abspath(pngFile)} {scale}x")

def run():
    config = getConfig()
    generated_svg = generateSVG(config)
    svg_file = saveSVG(generated_svg)
    png_file = os.path.join("export", "plaid-sheet.png")
    error_code = exportSVG(svg_file, png_file, config["output-scale"])

    print(f"{error_code=}")
    os.system(f"{png_file}")

if __name__ == "__main__": run()

