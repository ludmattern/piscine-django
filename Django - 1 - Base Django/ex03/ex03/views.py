from django.shortcuts import render


def generate_color_shades():
    columns = [
        {'name': 'Noir', 'rgb': (0, 0, 0)},      # Noir : (R, G, B) = (x, x, x)
        {'name': 'Rouge', 'rgb': (1, 0, 0)},     # Rouge : (R, G, B) = (x, 0, 0)
        {'name': 'Bleu', 'rgb': (0, 0, 1)},      # Bleu : (R, G, B) = (0, 0, x)
        {'name': 'Vert', 'rgb': (0, 1, 0)},      # Vert : (R, G, B) = (0, x, 0)
    ]
    
    rows = []
    for i in range(50):
        # Dégradé de 255 (clair) à 0 (foncé) sur 50 lignes
        # Chaque ligne a une valeur différente
        intensity = 255 - int((i * 255) / 49)
        
        row = []
        for col in columns:
            r = intensity if col['rgb'][0] == 1 else (intensity if col['name'] == 'Noir' else 0)
            g = intensity if col['rgb'][1] == 1 else (intensity if col['name'] == 'Noir' else 0)
            b = intensity if col['rgb'][2] == 1 else (intensity if col['name'] == 'Noir' else 0)
            
            # Format hexadécimal
            color = f'#{r:02x}{g:02x}{b:02x}'
            row.append(color)
        
        rows.append(row)
    
    return columns, rows


def index(request):
    columns, rows = generate_color_shades()
    
    context = {
        'columns': columns,
        'rows': rows,
    }
    return render(request, 'ex03/index.html', context)
