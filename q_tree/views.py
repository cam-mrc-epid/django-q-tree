from django.shortcuts import render
from q_tree.models import Questionnaire

def xml_view(request):
    results = {}
    if request.GET:
        id_var = request.GET['id']
    else:
        id_var = 'q_id'
    q = Questionnaire.objects.get(q_id=id_var)
    results['q'] = q
    return render(request, 'q_tree/fsq.xml', results, content_type="application/xhtml+xml")
