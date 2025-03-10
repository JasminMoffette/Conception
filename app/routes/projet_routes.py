from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.projet import Projet
from app import db

projet_bp = Blueprint("projet", __name__)

@projet_bp.route("/")
def projet():
    return render_template("projet.html")