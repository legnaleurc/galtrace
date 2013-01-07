{% load url from future %}
GalTrace.urls = {
	DELETE: '{% url 'galtrace.apps.shell.views.delete' %}',
	FETCH: '{% url 'galtrace.apps.shell.views.fetch' %}',
	LOAD: '{% url 'galtrace.apps.shell.views.load' %}',
	MOVE: '{% url 'galtrace.apps.shell.views.move' %}',
	SAVE: '{% url 'galtrace.apps.shell.views.save' %}',
};
