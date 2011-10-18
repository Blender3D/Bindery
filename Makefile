all:
	pyuic4 -i 2 -o gui.py gui.ui
	pyuic4 -i 2 -o project_files.py project_files.ui
	pyrcc4 -py2 -o resources_rc.py resources.qrc
	python2 main.py

clean:
	rm *.pyc
