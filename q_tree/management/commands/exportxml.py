from django.core.management.base import BaseCommand, CommandError
from q_tree.models import Questionnaire
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
import lxml

class Command(BaseCommand):
    args = '<q_id>'
    help = 'export questionnaire to xml'

    def handle(self, *args, **options):
        q = Questionnaire.objects.get(q_id=args[0])
        xml_out = render_to_string('q_tree/fsq.xml', {'q': q})
        soup = BeautifulSoup(xml_out, 'lxml')
        return soup.prettify()
