from context.cadence_label import detect_cadence_label


def test_detect_authentic_cadence_major():
    assert detect_cadence_label('V', 'I') == 'authentic-cadence'


def test_detect_authentic_cadence_minor():
    assert detect_cadence_label('V', 'i') == 'authentic-cadence-minor'


def test_detect_plagal_motion_major():
    assert detect_cadence_label('IV', 'I') == 'plagal-motion'


def test_detect_plagal_motion_minor():
    assert detect_cadence_label('iv', 'i') == 'plagal-motion-minor'


def test_detect_predominant_to_dominant_major():
    assert detect_cadence_label('ii', 'V') == 'predominant-to-dominant'


def test_detect_predominant_to_dominant_minor():
    assert detect_cadence_label('iv', 'V') == 'predominant-to-dominant-minor'


def test_detect_deceptive_cadence_major():
    assert detect_cadence_label('V', 'vi') == 'deceptive-cadence'


def test_detect_deceptive_cadence_minor():
    assert detect_cadence_label('V', 'VI') == 'deceptive-cadence-minor'


def test_detect_cadence_label_unknown_case():
    assert detect_cadence_label('iii', 'IV') is None
    
def test_detect_half_cadence():
    assert detect_cadence_label('I', 'V') == 'half-cadence'
    assert detect_cadence_label('ii', 'V') == 'predominant-to-dominant'
    assert detect_cadence_label('IV', 'V') == 'half-cadence'


def test_detect_dominant_to_mediant():
    assert detect_cadence_label('V', 'III') == 'dominant-to-mediant'
    
    