import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]
cx_Freeze.setup(
    name="Deep-Sea Adventures",
    options={"build_exe": {"packages": ["pygame", "playsound"],
                           "include_files": ["img/", "audio/"]}},
    description="Interactive survival game made with PyGame.",
    executables=executables
)

# Commands
# python setup.py build  ->  executable
# python setup.py bdist_msi  ->  installer
