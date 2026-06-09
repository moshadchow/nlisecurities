# Custom Color Palette for CKEditor 5
customColorPalette = [
    { 'color': 'hsl(0, 0%, 0%)',   'label': 'Black' },
    { 'color': 'hsl(0, 0%, 30%)',  'label': 'Dim grey' },
    { 'color': 'hsl(0, 0%, 60%)',  'label': 'Grey' },
    { 'color': 'hsl(0, 0%, 90%)',  'label': 'Light grey' },
    {
        'color': 'hsl(0, 0%, 100%)',
        'label': 'White',
        'hasBorder': True
    },
    { 'color': 'hsl(0, 75%, 60%)',  'label': 'Red' },
    { 'color': 'hsl(30, 75%, 60%)', 'label': 'Orange' },
    { 'color': 'hsl(60, 75%, 60%)', 'label': 'Yellow' },
    { 'color': 'hsl(90, 75%, 60%)', 'label': 'Light green' },
    { 'color': 'hsl(120, 75%, 60%)','label': 'Green' },
    { 'color': 'hsl(150, 75%, 60%)','label': 'Aquamarine' },
    { 'color': 'hsl(180, 75%, 60%)','label': 'Turquoise' },
    { 'color': 'hsl(210, 75%, 60%)','label': 'Light blue' },
    { 'color': 'hsl(240, 75%, 60%)','label': 'Blue' },
    { 'color': 'hsl(270, 75%, 60%)','label': 'Purple' },
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'link',
            'bulletedList', 'numberedList',
            'blockQuote'
        ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': [
            'heading', '|',
            'outdent', 'indent', '|',               # these handle nesting
            'bold', 'italic', 'link', 'underline', 'strikethrough',
            'code', 'subscript', 'superscript', 'highlight', '|',
            'codeBlock', 'sourceEditing', 'insertImage',
            'bulletedList', 'numberedList', 'multiLevelList', 'todoList', '|',
            'blockQuote', 'imageUpload', '|',
            'alignment',
            'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor',
            'mediaEmbed', 'removeFormat',
            'insertTable', '|',
            'undo', 'redo'
        ],

        # Font size dropdown
        'fontSize': {
            'options': [8, 10, 12, 14, 18, 24, 36],
            'supportAllValues': True
        },

        # List / sub-bullet configuratTinyion
        'list': {
            'properties': {
                'styles': 'true',      # disc / circle / square / decimal / etc.
                'startIndex': 'true',  # start from 3, 4, etc.
                'reversed': 'true',    # reverse numbering
            }
        },

        'alignment': {
            'options': ['left', 'center', 'right', 'justify']
        },

        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft',
                'imageStyle:alignRight',
                'imageStyle:alignCenter',
                'imageStyle:side',
                'imageStyle:full', '|'
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },

        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells',
                'tableProperties', 'tableCellProperties'
            ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },

        'heading': {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    }
}
