all: 2

2:
	pyuic4 -i 2 -o ui/gui.py ui/gui.ui
	pyuic4 -i 2 -o ui/project_files.py ui/project_files.ui
	pyrcc4  -o ui/resources_rc.py ui/resources.qrc
	python2 main.py

3:
	pyuic4 --from-imports -i 2 -o ui/gui.py ui/gui.ui
	pyuic4 --from-imports -i 2 -o ui/project_files.py ui/project_files.ui
	pyrcc4 -py3 -o ui/resources_rc.py ui/resources.qrc
	python3 main.py

clean:
	rm *.pyc
