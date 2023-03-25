Param (
    [Parameter(Mandatory)]
    $Year
    )
If((test-path -PathType container $Year))
{
    return
}

New-Item -ItemType Directory -Path $Year
python -m venv .\$Year\.venv
copy .\Activate.tmpl .\$Year\.venv\Scripts\Activate.ps1
deactivate
.$Year\.venv\Scripts\activate
New-Item -ItemType File -Path $Year\.venv\.gitignore -Value "*"
pip install -e d:\git\advent-cli\
New-Item -ItemType Directory -Path $Year\aoctoolbox
Copy-Item -Path .\latest_aoc_toolbox\* -Recurse -Destination .\$Year\aoctoolbox -Container
 
pip install -e .\$Year\aoctoolbox\
pip install networkx
pip install matplotlib
pip install numpy
pip install pygame

advent year $Year