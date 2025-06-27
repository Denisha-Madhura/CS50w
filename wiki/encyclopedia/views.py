from django.shortcuts import render
import markdown2
import os
from django import forms
from django.conf import settings
from . import util
from django.shortcuts import redirect
import random

class MarkdownForm(forms.Form):
    title = forms.CharField(max_length = 200, widget = forms.TextInput(attrs={'placeholder': "Enter title here", "style":"width: 100%; background-color: rgba(29,29,29,0.25); color: hsl(0,0%,100%);"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Enter markdown content here", "style":"width: 100%; background-color: rgba(29,29,29,0.25);color: hsl(0,0%,100%);"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



ENTRIES_DIR = os.path.join(settings.BASE_DIR, 'entries')

def entry(request, entry_name):
    # Sanitize filename
    filename = f"{entry_name}.md"
    filepath = os.path.join(ENTRIES_DIR, filename)


    # Read and parse markdown
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_md = f.read()
        html = markdown2.markdown(raw_md)

    return render(request,  "encyclopedia/entry.html", {'content': html, 'title': entry_name})



def create(request):
    title = ''
    html_output=''
    if request.method == "POST":
        form = MarkdownForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            md_content = form.cleaned_data['content']
            filename = f"{title.strip().replace(' ', '_')}.md"
            filepath = os.path.join(ENTRIES_DIR, filename)

            if os.path.exists(filepath):
                error = "A page with the title already exists"
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(md_content)


            html_output = markdown2.markdown(md_content)
    else:
        form = MarkdownForm()
    
    return render(request,  "encyclopedia/create.html", {
        'form': form,
        'html_output':html_output,
        'title': title,
        'editing':False
    })


def random_page(request):
    entries = [f for f in os.listdir(ENTRIES_DIR) if f.endswith('.md')]

    if not entries:
        return redirect('index') 

    random_file = random.choice(entries)
    title = os.path.splitext(random_file)[0]

    
    return redirect('entry', entry_name=title)

def search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return redirect('index')

    entries = [f[:-3] for f in os.listdir(ENTRIES_DIR) if f.endswith('.md')]

    entries.sort()

    for entry in entries:
        if entry.lower() == query.lower():
            return redirect('entry', entry_name=entry)


    for entry in entries:
        if query.lower() in entry.lower():
            return redirect('entry', entry_name=entry)

    return render(request, 'encyclopedia/error.html', {
        'message': f"No entry found for '{query}'."
    })


def edit(request, entry_name):
    filepath = os.path.join(ENTRIES_DIR, f"{entry_name}.md")

    if request.method == "POST":
        new_content = request.POST.get("content", "")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return redirect('entry', entry_name=entry_name)

    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            current_content = f.read()

        form = MarkdownForm(initial={
            'title': entry_name,
            'content': current_content
        })

        return render(request, "encyclopedia/create.html", {
            'form': form,
            'title': entry_name,
            'editing': True
        })

    else:
        return render(request, "encyclopedia/error.html", {
            'message': "Entry not found."
        })


