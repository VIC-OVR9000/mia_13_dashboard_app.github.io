from flask import Flask, render_template, jsonify
import yfinance as yf
import pandas as pd
import math

app = Flask(__name__)

# MIA-13 SYSTEM ARCHITECTURE (Integer Optimized)
MIA_CONFIG = {
    'GOOGL': {'shares': 9,  'strike': 150, 'type': 'long',    'core': 'V'},
    'MSFT':  {'shares': 6,  'strike': 400, 'type': 'long',    'core': 'V'},
    'ORCL':  {'shares': 12, 'strike': 160, 'type': 'long',    'core': 'V'},
    'META':  {'shares': 3,  'strike': 450, 'type': 'long',    'core': 'Beta'},
    'AMZN':  {'shares': 12, 'strike': 180, 'type': 'long',    'core': 'Beta'},
    'TTD':   {'shares': 10, 'strike': 90,  'type': 'long',    'core': 'Beta'},
    'PG':    {'shares': 11, 'strike': 170, 'type': 'short',   'core': 'Omega'},
    'KO':    {'shares': 26, 'strike': 65,  'type': 'short',   'core': 'Omega'},
    'WMT':   {'shares': 18, 'strike': 130, 'type': 'short',   'core': 'Omega'},
    'GLD':   {'shares': 4,  'strike': 250, 'type': 'short',   'core': 'Entropy'},
    'TLT':   {'shares': 12, 'strike': 95,  'type': 'short',   'core': 'Entropy'},
    'VIXY':  {'shares': 84, 'strike': 15,  'type': 'long',    'core': 'Entropy'}
}
LATINUM_STASIS = 2939.44

@app.route('/')
def index():
    return render_template('dash2.html')

@app.route('/api/data')
def get_data():
    tickers = list(MIA_CONFIG.keys()) + ['SPY']
    # Fetch live snapshots
    data = yf.download(tickers, period='1d', interval='1m')['Close'].iloc[-1]
    
    fleet_value = LATINUM_STASIS
    feedback_iv = 0
    ship_stats = []

    for t, meta in MIA_CONFIG.items():
        price = data[t]
        val = price * meta['shares']
        fleet_value += val
        
        # Feedback Logic (Intrinsic Value)
        iv = 0
        if meta['type'] == 'long':
            iv = max(0, price - meta['strike']) * meta['shares']
        else:
            iv = max(0, meta['strike'] - price) * meta['shares']
        
        feedback_iv += iv
        ship_stats.append({
            'ticker': t, 'price': round(price, 2), 
            'core': meta['core'], 'val': round(val, 2),
            'iv': round(iv, 2)
        })

    spy_price = data['SPY']
    
    return jsonify({
        'fleet_index': round(fleet_value / 100, 2), # Normalized Index
        'total_value': round(fleet_value, 2),
        'feedback_iv': round(feedback_iv, 2),
        'spy': round(spy_price, 2),
        'ships': ship_stats
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)


