const ProjectStructure = () => {
  return (
    <div className="p-6 bg-gray-50 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Project Structure</h2>
      <pre className="bg-gray-800 text-green-400 p-4 rounded overflow-auto max-h-[500px]">
        {`quantum_defi/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── quantum_defi/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   ├── forms.py
│   └── migrations/
├── blockchain/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── ethereum.py
│   │   └── transaction.py
│   └── migrations/
├── quantum_crypto/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── oqs_wrapper.py
│   │   └── key_management.py
│   └── migrations/
├── ai_security/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   ├── ml_models/
│   │   ├── __init__.py
│   │   ├── anomaly_detection.py
│   │   └── threat_models.py
│   └── migrations/
├── api/
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    ├── accounts/
    ├── blockchain/
    └── dashboard/`}
      </pre>
    </div>
  )
}

export default ProjectStructure

