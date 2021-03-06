from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ordermanager.models import Order, Contact
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from ordermanager.forms import OrderForm, ContactForm
from datetime import datetime


class AboutView(TemplateView):
    template_name = 'about.html'


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter().order_by('-date')


class OrderDetailView(DetailView):
    model = Order


class OrderHandlingTag(DetailView):
    model = Order
    template_name = 'handling_tag.html'


class CreateOrderView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/order_detail.html'
    form_class = OrderForm
    model = Order

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.date = datetime.now()
        self.object.save()
        # Captures newly saved objects information for emails.
        order_data = {'order_pk': self.object.pk,
                      'order_number': self.object.order_number,
                      'customer': self.object.customer,
                      'product_name': self.object.product_name,
                      'design_code': self.object.design_code,
                      'order_reason': self.object.order_reason,
                      'process_date': self.object.process_date,
                      'ship_date': self.object.ship_date,
                      'sequence_numbers': self.object.sequence_numbers,
                      'tooling_status': self.object.tooling_status,
                      'programming_status': self.object.programming_status,
                      'order_notes': self.object.order_notes,
                      'engineering_framing_setup': self.object.engineering_framing_setup,
                      'engineering_panel_setup': self.object.engineering_panel_setup,
                      'engineering_lipping_setup': self.object.engineering_lipping_setup,
                      'engineering_assembly': self.object.engineering_assembly,
                      'engineering_options': self.object.engineering_options,
                      'engineering_other': self.object.engineering_other}
        send_order_emails(order_data, "New")
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/order_detail.html'
    form_class = OrderForm
    model = Order

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        # Captures newly saved objects information for emails.
        order_data = {'order_pk': self.object.pk,
                      'order_number': self.object.order_number,
                      'customer': self.object.customer,
                      'product_name': self.object.product_name,
                      'design_code': self.object.design_code,
                      'order_reason': self.object.order_reason,
                      'process_date': self.object.process_date,
                      'ship_date': self.object.ship_date,
                      'sequence_numbers': self.object.sequence_numbers,
                      'tooling_status': self.object.tooling_status,
                      'programming_status': self.object.programming_status,
                      'order_notes': self.object.order_notes,
                      'engineering_framing_setup': self.object.engineering_framing_setup,
                      'engineering_panel_setup': self.object.engineering_panel_setup,
                      'engineering_lipping_setup': self.object.engineering_lipping_setup,
                      'engineering_assembly': self.object.engineering_assembly,
                      'engineering_options': self.object.engineering_options,
                      'engineering_other': self.object.engineering_other}
        send_order_emails(order_data, "Update")
        return super().form_valid(form)


class ContactListView(ListView):
    model = Contact

    def get_queryset(self):
        return Contact.objects.filter(active=True).order_by('site', 'last_name')


class ContactDetailView(DetailView):
    model = Contact


class AddContactView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/contact_detail.html'
    form_class = ContactForm
    model = Contact


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'ordermanager/contact_detail.html'
    form_class = ContactForm
    model = Contact


def send_order_emails(order_data, process):
    if process == "New":
        email_subject = f"Special Order: {order_data['order_number']} is ready!"
    else:
        email_subject = f"Special Order UPDATE: {order_data['order_number']} has been UPDATED!"
    html_message_a = render_to_string('email_template_a.html', order_data)
    html_message_b = render_to_string('email_template_b.html', order_data)
    plain_message_a = strip_tags(html_message_a)
    plain_message_b = strip_tags(html_message_b)
    from_email = 'sender@yourdomain.com'
    to_a = []
    to_b = []
    contacts = Contact.objects.filter(active=True)
    for contact in contacts:
        if contact.site == 'Facility A':
            to_a.append(contact.email_address)
        else:
            to_b.append(contact.email_address)

    send_mail(email_subject, plain_message_b, from_email, to_b, html_message=html_message_b)
    send_mail(email_subject, plain_message_a, from_email, to_a, html_message=html_message_a)
