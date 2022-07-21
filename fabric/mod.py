import os

from errors import ModFolderNotFound, ModFileNotFound

class Mod:
    def __init__(self, name:str, description:str, author:str, *, project_license:str = None, source:str = None):
        self.name = name
        self.descriptionv = description
        self.author = author
        self.license = license
        self.source = source
        self.fabric_mod_json = '''
{
    "schemaVersion": 1,
    "id": "{modID}",
    "version": "${{version}}",

    "name": "{name}",
    "description": "{desc}",
    "authors": [
        "{author}"
    ],
    "contact": {
        "homepage": "https://fabricmc.net/",
        "sources": "{source}"
    },

    "license": "{project_license}",
    "icon": "assets/modid/icon.png",

    "environment": "*",
    "entrypoints": {
        "main": [
            "net.{author_re}.{name_re}.{name_re_1}"
        ]
    },
    "mixins": [
        "modid.mixins.json"
    ],

    "depends": {
        "fabricloader": ">=0.14.6",
        "fabric": "*",
        "minecraft": "~1.19",
        "java": ">=17"
    },
    "suggests": {
        "another-mod": "*"
    }
}
    '''.format(name=self.name, desc=self.description, author=self.author, project_license="None" if self.project_license==None else self.project_license, modID=self.__class__.__name__.lower(), source=self.source, name_re=self.name.replace(" ", "_"), name_re_1=self.name.replace(" ", "_").replace("-", "_"), author_re=self.author.replace(" ", "_"))

    
    def registerMod(self):
        path = self.__class__.__name__
        isdir = os.path.isdir(path)
        if isdir:
            try:
                with open(f"{self.__class__.__name__}/src/main/resources/fabric.mod.json", "w") as file:
                    file.write(self.fabric_mod_json)
                    
                    try:
                        os.rename(f"{self.__class__.__name__}/src/main/java/net/fabricmc", f"{self.__class__.__name__}/src/main/java/net/{self.author.replace(' ', '_')}")
                    except:
                        raise ModFileNotFound(f"Cannot find {self.__class__.__name__}/src/main/java/net/{self.author.replace(' ', '_')}")
                    
                    for root, dirs, files in os.walk("/mydir"):
                        for file in files:
                            with open(file, "r+") as f:
                                data = f.read()
                                data.replace("fabricmc", f"{self.author.replace(' ', '_')}")
                    
                    
            except:
                raise ModFileNotFound(f"Cannot find {self.__class__.__name__}/src/main/resources/fabric.mod.json")
        else:
            raise ModFolderNotFound("There is no Fabric Mod Folder")