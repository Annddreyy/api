from flask import Flask, jsonify, request
import json

with open('nodes.json', 'r', encoding='utf-8') as file:
    n = json.load(file)
nodes = [n]

app = Flask(__name__)

app.config['SECRET_KEY'] = 'wd34j353l6b34o6b2g204nc70b0xql4j2n5'


def find_node(node_id):
    node = None
    for N in nodes[0]['nodes']:
        if N['id'] == node_id:
            node = N
            break
    return node


def find_dialog(dialog_id):
    dialog = None
    for N in nodes[0]['nodes']:
        for d in N['dialogs']:
            if d['id'] == dialog_id:
                dialog = d
                break
        if dialog:
            break
    return dialog


@app.route('/api', methods=['GET'])
def get_all():
    return jsonify(nodes)


@app.route('/api/nodes/<int:node_id>', methods=['GET'])
def get_node(node_id):
    node = find_node(node_id)
    if node:
        return jsonify(node)
    return {'message': 'no nodes with this id'}, 400


@app.route('/api/dialogs/<int:dialog_id>', methods=['GET'])
def get_dialog(dialog_id):
    dialog = find_dialog(dialog_id)
    if dialog:
        return jsonify(dialog)
    return {'message': 'no dialog with this id'}, 400


@app.route('/api/dialogs/<int:dialog_id>/variants', methods=['GET'])
def get_variants(dialog_id):
    dialog = find_dialog(dialog_id)
    if dialog:
        return jsonify(dialog['variants'])
    return {'message': 'no dialog with this id'}, 400


@app.route('/api/nodes/<int:node_id>/location', methods=['GET'])
def get_node_location(node_id):
    node = find_node(node_id)
    if node:
        return jsonify(node['location'])
    return {'message': 'no nodes with this id'}, 400


@app.route('/api/nodes', methods=['POST'])
def add_node():
    try:
        new_node = request.json
        nodes[0]['nodes'].append(new_node)
        return jsonify(nodes)
    except:
        return {'message': 'cant add new node'}, 400


@app.route('/api/nodes/<int:node_id>', methods=['POST'])
def add_dialog(node_id):
    add = False
    new_node = request.json
    for N in nodes[0]['nodes']:
        if N['id'] == node_id:
            N['dialogs'].append(new_node)
            add = True
    if add:
        return jsonify(nodes)
    else:
        return {'message': 'cant add new dialog'}, 400


@app.route('/api/dialogs/<int:dialog_id>', methods=['POST'])
def add_variant(dialog_id):
    add = False
    new_variant = request.json
    for N in nodes[0]['nodes']:
        for d in N['dialogs']:
            if d['id'] == dialog_id:
                d['variants'].append(new_variant)
                add = True
    if add:
        return jsonify(nodes)
    else:
        return {'message': 'cant add new variant'}, 400


@app.route('/api/nodes/<int:node_id>', methods=['PUT'])
def update_node(node_id):
    node = find_node(node_id)
    if node:
        node.update(request.json)
        return jsonify(node)
    return {'message': 'cant find node with this id'}, 400


@app.route('/api/dialogs/<int:dialog_id>', methods=['PUT'])
def update_dialog(dialog_id):
    dialog = find_dialog(dialog_id)
    if dialog:
        dialog.update(request.json)
        return jsonify(dialog)
    return {'message': 'cant find dialog with this id'}, 400


@app.route('/api/dialogs/<int:dialog_id>', methods=['PUT'])
def update_variant(dialog_id):
    dialog = find_dialog(dialog_id)
    if dialog:
        dialog['variants'].update(request.json)
        return jsonify(dialog)
    return {'message': 'cant find dialog with this id'}, 400


@app.route('/api/nodes/<int:node_id>/location', methods=['PUT'])
def update_location(node_id):
    node = find_node(node_id)
    if node:
        node['location'].update(request.json)
        return jsonify(node)
    return {'message': 'cant find dialog with this id'}, 400


@app.route('/api/nodes/<int:node_id>', methods=['DELETE'])
def delete_node(node_id):
    node = find_node(node_id)
    if node:
        nodes[0]['nodes'].remove(node)
        return jsonify(nodes)
    return {'message': 'no node with this id'}, 400


@app.route('/api/dialogs/<int:dialog_id>', methods=['DELETE'])
def delete_dialog(dialog_id):
    delete = False
    for N in nodes[0]['nodes']:
        for d in N['dialogs']:
            if d['id'] == dialog_id:
                N['dialogs'].remove(d)
                delete = True
                break
        if delete:
            return jsonify(N)
    return {'message': 'cant find dialog with this id'}, 400


@app.route('/api/dialogs/<int:dialog_id>/variants', methods=['DELETE'])
def delete_variant(dialog_id):
    delete = False
    for N in nodes[0]['nodes']:
        for d in N['dialogs']:
            if d['id'] == dialog_id:
                try:
                    d['variants'].remove(request.json)
                    delete = True
                    break
                except:
                    return {'message': 'dialog doesnt have this variant'}
        if delete:
            return jsonify(N)
    return {'message': 'cant find dialog with this id'}, 400


if __name__ == '__main__':
    app.run(debug=True)
