def generate_html_report(results, recommendation, output_file="report.html"):
    
    # 🏆 Sort models by DRS
    ranked = sorted(
        results.items(),
        key=lambda x: x[1].get("drs_score", 0),
        reverse=True
    )

    # 📊 Build table rows
    rows = ""
    for i, (model, data) in enumerate(ranked, 1):
        m = data["metrics"]

        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{model}</td>
            <td>{m.get('accuracy', 0):.3f}</td>
            <td>{m.get('semantic', 0):.3f}</td>
            <td>{m.get('reliability', 0):.3f}</td>
            <td>{m.get('safety', 0):.3f}</td>
            <td>{m.get('consistency', 0):.3f}</td>
            <td>{m.get('variance', 0):.3f}</td>
            <td>{m.get('latency', 0):.2f}</td>
            <td>{data.get('drs_score', 0):.3f}</td>
        </tr>
        """

    # 🚨 Risks
    risks_html = "".join([f"<li>{r}</li>" for r in recommendation["risks"]])

    # 🧠 HTML Template
    html = f"""
    <html>
    <head>
        <title>OpenVals Report</title>
        <style>
            body {{
                font-family: Arial;
                padding: 20px;
                background: #f4f6f8;
            }}
            h1 {{ color: #222; }}
            .card {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                text-align: center;
            }}
            th {{
                background: #222;
                color: white;
            }}
            .highlight {{
                color: green;
                font-weight: bold;
            }}
        </style>
    </head>

    <body>

    <h1>🚀 OpenVals AI Evaluation Report</h1>

    <div class="card">
        <h2>🧠 Recommendation</h2>
        <p><b>Best Model:</b> <span class="highlight">{recommendation['recommended_model']}</span></p>
        <p><b>Score:</b> {recommendation['score']}</p>
        <p><b>DRS:</b> {recommendation['drs']}</p>
        <p><b>Confidence:</b> {recommendation['confidence']}</p>

        <p><b>Why:</b> {recommendation['reason']}</p>
        <p><b>Trade-offs:</b> {recommendation['tradeoffs']}</p>

        <p><b>Risks:</b></p>
        <ul>{risks_html}</ul>
    </div>

    <div class="card">
        <h2>📊 Model Leaderboard</h2>

        <table>
            <tr>
                <th>Rank</th>
                <th>Model</th>
                <th>Acc</th>
                <th>Sem</th>
                <th>Rel</th>
                <th>Safe</th>
                <th>Cons</th>
                <th>Var</th>
                <th>Latency(ms)</th>
                <th>DRS</th>
            </tr>

            {rows}

        </table>
    </div>

    </body>
    </html>
    """

    # 💾 Save file
    with open(output_file, "w") as f:
        f.write(html)