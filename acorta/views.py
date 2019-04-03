from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponsePermanentRedirect, HttpResponseNotAllowed
from django.views.decorators.csrf import get_token
from .models import NewURL

# HTML pages

PAGE_MAIN_GET = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h2>Aplicacion web acortadora de URLs</h2>
    <p>Escribe aqui la web que quieres acortar:</p><p>
    <form action="/" method="post">
        URL: <input type="text" name="url" value="https://www.aulavirtual.urjc.es"><br><br>
        <input type="hidden" name="csrfmiddlewaretoken" value="{token}"/>
        <input type="submit" value="Enviar">
    </form></p><p>
    <h4>---Lista de enlaces acortados---</h4>
    <table>
        <tr>
            <th>URL real</th>
            <th>URL acortada</th>
        <tr>
        {table}
    </table>
  </body>
</html>
"""

PAGE_ERROR = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="Refresh" content="10; url=http://127.0.0.1:{port}/" />
  </head>
  <body>
    <h2>Aplicacion web acortadora de URLs</h2>
    <p>{msg}</p>
  </body>
</html>
"""

PAGE_RETURN_URL = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h2>Aplicacion web acortadora de URLs</h2>
    <p>URL introducida: <a href={url1}>{url1}</a></p>
    <p>URL acortada: <a href={url2}>{url2}</a></p>
  </body>
</html>
"""


def number(request, numero):
    if request.method == 'GET':
        url_to_search = "http://127.0.0.1:" + request.META['SERVER_PORT'] + "/" + str(numero)

        if NewURL.objects.filter(URL_short=url_to_search).exists():
            url_long = NewURL.objects.get(URL_short=url_to_search).URL_long

            return HttpResponsePermanentRedirect(url_long)

        else:
            http_msg = ("El numero introducido no está almacenado en la lista. Introduzca otro numero" +
                        "<br/>" + "Se redigira a la pagina principal")

            return HttpResponseNotFound(PAGE_ERROR.format(port=request.META['SERVER_PORT'], msg=http_msg))

    else:
        http_msg = ("El método introducido no está soportado para el recurso requerido" +
                    "<br/>" + "Se redigira a la pagina principal")

        return HttpResponseNotAllowed(PAGE_ERROR.format(port=request.META['SERVER_PORT'], msg=http_msg))


def check_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return "http://" + url


def index(request):
    print("Entrando a la funcion index")
    http_msg = ""

    csrf_token = get_token(request)

    if request.method == 'GET':
        url_stored = NewURL.objects.all()

        for url in url_stored:
            http_msg += ("<tr><td><a href=" + url.URL_long + ">" + url.URL_long + "</a></td>" +
                         "<td><a href=" + url.URL_short + ">" + url.URL_short + "</a>" + "</td></tr>")

        return HttpResponse(PAGE_MAIN_GET.format(token=csrf_token, table=http_msg))

    elif request.method == 'POST':
        try:
            url = request.POST['url']
        except KeyError:
            http_msg = ("El formulario introducido no proviene de la pagina correcta." +
                        "Se redirigira a la pagina principal")

            return HttpResponseBadRequest(PAGE_ERROR.format(port=request.META['SERVER_PORT'], msg=http_msg))

        url_to_add = check_url(url)

        if NewURL.objects.filter(URL_long=url_to_add).exists():
            url_short = NewURL.objects.get(URL_long=url_to_add).URL_short
        else:
            url_count = NewURL.objects.count()
            url_short = "http://127.0.0.1:" + request.META['SERVER_PORT'] + "/" + str(url_count)
            new_url_obj = NewURL(URL_long=url_to_add, URL_short=url_short)
            new_url_obj.save()

        return HttpResponse(PAGE_RETURN_URL.format(url1=url_to_add, url2=url_short))

    else:
        http_msg = "El metodo enviado no esta soportado por el servidor. Se redirigira a la pagina principal"

        return HttpResponseNotAllowed(PAGE_ERROR.format(port=request.META['SERVER_PORT'], msg=http_msg))


def error(request):
    http_msg = "El recurso introducido no existe. Se redirigira a la pagina principal"

    return HttpResponseNotFound(PAGE_ERROR.format(port=request.META['SERVER_PORT'], msg=http_msg))
