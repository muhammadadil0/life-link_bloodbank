"""
Main routes for LifeLink Blood Bank Management System
"""

from flask import Blueprint, render_template, flash, redirect, url_for
from models import Donor, Feedback, db
from forms import FeedbackForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Homepage route"""
    # Query the actual number of active donors
    from models import Donor
    active_donors_count = Donor.query.filter_by(is_available=True).count()
    stats = [
        {"label": "Active Donors", "value": str(active_donors_count), "icon": "users", "gradient": "from-blue-500 to-blue-600"},
        {"label": "Emergency Support", "value": "24/7", "icon": "clock", "gradient": "from-purple-500 to-violet-600"}
    ]
    return render_template('index.html', stats=stats)

@main_bp.route('/donors')
def donors():
    """Donors listing page"""
    donors_list = Donor.query.all()
    total_donors = Donor.query.count()
    active_donors = Donor.query.filter_by(is_available=True).count()
    return render_template('donors.html', donors=donors_list, total_donors=total_donors, active_donors=active_donors)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)

@main_bp.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')

@main_bp.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('terms.html')

@main_bp.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html') 