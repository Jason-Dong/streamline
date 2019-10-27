from utils import get_val_from_request, get_doc, add_doc, exists


def add_party(request):
    name = get_val_from_request(request, 'name')
    if name and not exists('parties', name):
        add_doc("parties-all", name)
        add_doc("parties-filtered", name)
        return "success"
    return "failure"

