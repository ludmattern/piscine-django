from django.shortcuts import render, redirect
from django.conf import settings
from .forms import InputForm
from datetime import datetime
import os


def read_history():
    """Lit l'historique depuis le fichier de logs."""
    history = []
    log_file = settings.LOG_FILE_PATH
    
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # Format: [timestamp] text
                    if line.startswith('['):
                        try:
                            end_bracket = line.index(']')
                            timestamp = line[1:end_bracket]
                            text = line[end_bracket + 2:]
                            history.append({
                                'timestamp': timestamp,
                                'text': text
                            })
                        except (ValueError, IndexError):
                            pass
    return history


def write_to_log(text):
    """Écrit une entrée dans le fichier de logs."""
    log_file = settings.LOG_FILE_PATH
    
    # Créer le dossier si nécessaire
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {text}\n')
    
    return timestamp


def index(request):
    """Vue principale avec formulaire et historique."""
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            write_to_log(text)
            return redirect('ex02:index')
    else:
        form = InputForm()
    
    history = read_history()
    
    context = {
        'form': form,
        'history': history,
    }
    return render(request, 'ex02/index.html', context)
