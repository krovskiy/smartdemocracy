from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

API_ENDPOINT_GRAPH = "https://app.trustservista.com/api/rest/v2/graph"
API_ENDPOINT_TRUST = "https://app.trustservista.com/api/rest/v2/trustlevel"
API_KEY = "d4f388d353b44266aa075e2c5cd2b48b"  # hardcoded crazy
HEADERS = {
    "X-TRUS-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cache-Control": "no-cache"
}


def get_graph(content_uri):
    data = {
        "content": "EMPTY",
        "contentUri": content_uri,
        "language": "eng"
    }
    response = requests.post(API_ENDPOINT_GRAPH, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}


def get_trust(content_uri):
    data = {
        "content": "EMPTY",
        "contentUri": content_uri,
        "language": "eng"
    }
    response = requests.post(API_ENDPOINT_TRUST, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}


def sort_graph_nodes(graph_result):
    graph_result['graphNodes'] = sorted(
        graph_result['graphNodes'],
        key=lambda x: min(
            article.get('publishTime', '9999-99-99')
            for article in x.get('articleGraphNodes', [])
        )
    )

    for node in graph_result['graphNodes']:
        node['articleGraphNodes'] = sorted(
            node.get('articleGraphNodes', []),
            key=lambda article: article.get('publishTime', '9999-99-99')
        )

    return graph_result


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    first_publisher = None
    if request.method == 'POST':
        content_uri = request.form.get('contentUri')
        graph_result = get_graph(content_uri)
        trust_result = get_trust(content_uri)
        graph_result = sort_graph_nodes(graph_result)

        print(json.dumps(graph_result, indent=4))

        earliest_time = None
        for node in graph_result.get('graphNodes', []):
            for article in node.get('articleGraphNodes', []):
                publish_time = article.get('publishTime')
                if publish_time:
                    if earliest_time is None or publish_time < earliest_time:
                        earliest_time = publish_time
                        first_publisher = {
                            "title": article.get('title'),
                            "source": article.get('source'),
                            "publishTime": publish_time,
                            "url": article.get('url')
                        }

        result = {
            "graph": graph_result,
            "trust": trust_result
        }

        graph_result['graphNodes'] = sorted(graph_result['graphNodes'], key=lambda x: x['articleGraphNodes'][0]['publishTime'])

    return render_template_string('''
    <!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f4f6f9;
            font-family: 'Inter', sans-serif;
        }
        .card {
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: scale(1.02);
        }
        .form-control {
            border-radius: 8px;
        }
        .btn-primary {
            background-color: #3b82f6;
            border-color: #3b82f6;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            background-color: #2563eb;
            border-color: #2563eb;
        }
        .container {
            max-width: 800px;
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            margin-top: 50px;
        }
        h1, h2 {
            color: #2c3e50;
        }
        .trust-level-badge {
            font-size: 1.2em;
            font-weight: bold;
            padding: 10px;
            border-radius: 8px;
            background-color: #e6f2ff;
            color: #2563eb;
        }
        .progress-bar-custom {
            transition: width 0.5s ease-in-out;
        }
    </style>
    <title>Smartdemocracy Source</title>
</head>
<body>
    <div class="container rounded shadow">
        <h1 class="text-center mb-4" style="
    font-size: 3rem;
    background: linear-gradient(90deg, #3b82f6, #b026ff, #3b82f6);
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    background-clip: text;
    animation: shine 3s linear infinite;
    transition: all 0.3s ease;
    cursor: pointer;"
    onclick="window.location.href='/';">
    SMARTDEMOCRACY
</h1>
<style>
    @keyframes shine {
        to { background-position: 200% center; }
    }
    h1:hover {
        transform: scale(1.05);
    }
</style>
        <form method="post" class="mb-4">
            <div class="form-group">
                <label for="contentURL" class="form-label">Content URL:</label>
                <div class="input-group">
                    <input type="text" class="form-control" id="contentUri" name="contentUri" 
                           placeholder="Paste your link here!" required>
                    <button type="submit" class="btn btn-primary">Analyze</button>
                </div>
            </div>
        </form>
                                  
        {% if first_publisher %}
            <div class="row mt-4">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header bg-info text-white">
                            <h3 class="mb-0">First Publisher</h3>
                        </div>
                        <div class="card-body">
                            <h4>{{ first_publisher.title }}</h4>
                            <p>
                                <strong>Source:</strong> {{ first_publisher.source }}<br>
                                <strong>Published:</strong> {{ first_publisher.publishTime }}
                            </p>
                            <a href="{{ first_publisher.url }}" class="btn btn-info" target="_blank">Original Article</a>
                        </div>
                    </div>
                </div>
            </div>
        {% endif %}

        {% if result %}
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h3 class="mb-0">Trust Level</h3>
                        </div>
                        <div class="card-body">
                            <div class="trust-level-badge text-center mb-3">
                                Trust Level: {{ result.trust.trustLevel }}
                            </div>
                            <div class="row">
                                {% for component in result.trust.trustLevelComponent.trustLevelComponents %}
                                    {% if component.type not in ['author', 'entity'] %}
                                        <div class="col-md-4 mb-2">
                                            <div class="card">
                                                <div class="card-body">
                                                    <h5>
                                                        {% if component.type == 'source' %}
                                                            Source Credibility
                                                        {% elif component.type == 'noclickbait' %}
                                                            Content Quality
                                                        {% elif component.type == 'sentiment' %}
                                                            Emotional Neutrality
                                                        {% else %}
                                                            {{ component.type }}
                                                        {% endif %}
                                                    </h5>
                                                    <div class="progress" style="height: 20px;">
                                                        <div class="progress-bar progress-bar-custom" 
                                                             role="progressbar" 
                                                             style="width: {{ (component.score * 100) }}%; 
                                                                    background-color: {% if component.score < 0.33 %}#dc3545{% elif component.score < 0.66 %}#ffc107{% else %}#28a745{% endif %};" 
                                                             aria-valuenow="{{ component.score * 100 }}" 
                                                             aria-valuemin="0" 
                                                             aria-valuemax="100">
                                                            {% if component.type == 'sentiment' %}
                                                                {% if component.score > 0.5 %}
                                                                    Positive
                                                                {% else %}
                                                                    Negative
                                                                {% endif %}
                                                            {% else %}
                                                                {{ "%.2f"|format(component.score * 100) }}%
                                                            {% endif %}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    {% endif %}
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header bg-secondary text-white">
                            <h3 class="mb-0">Content Graph</h3>
                        </div>
                        <div class="card-body">
                            {% for node in result.graph.graphNodes %}
                                <div class="card mb-3">
                                    <div class="card-header">Level {{ node.level }}</div>
                                    <div class="card-body">
                                        {% for article in node.articleGraphNodes %}
                                            <div class="mb-3 p-3 border rounded">
                                                <h5>{{ article.title }}</h5>
                                                <p>
                                                    <strong>Source:</strong> {{ article.source }}<br>
                                                    <strong>Published:</strong> {{ article.publishTime }}
                                                </p>
                                                <a href="{{ article.url }}" class="btn btn-sm btn-outline-primary" target="_blank">Read more</a>
                                            </div>
                                        {% endfor %}
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    ''', result=result, first_publisher=first_publisher)


if __name__ == '__main__':
    app.run(debug=True)