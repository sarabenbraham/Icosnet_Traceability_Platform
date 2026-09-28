import os
import re

form_path = r"c:\Users\ASUS\Icosnet_Traceability_Platform\backend\templates\application_sheet\fiche_form.html"
with open(form_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace form.field with form.fiche.field for the existing fields
fields_to_prefix = ['nom_application', 'domaine_fonctionnel', 'criticite', 'statut', 'description']
for field in fields_to_prefix:
    content = content.replace(f'form.{field}', f'form.fiche.{field}')

# Remove the "Sections verrouillées" block because we now show everything
content = re.sub(r'<!-- Sections verrouillées.*?</div>', '', content, flags=re.DOTALL)

# Add the new sections right before <!-- Actions -->
new_sections = """
    <!-- Section : Infrastructure -->
    <div class="form-card fade-in delay-4" style="margin-bottom:24px;">
      <div class="form-section-title">
        <svg width="16" height="16" fill="none" stroke="#2d5be3" stroke-width="2" viewBox="0 0 24 24" style="display:inline;margin-right:8px;vertical-align:middle;"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
        Infrastructure
      </div>
      <div class="form-grid">
        {% for field in form.infrastructure %}
        <div class="form-group">
          <label for="{{ field.id_for_label }}">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div class="field-error">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
    </div>

    <!-- Section : Contrat -->
    <div class="form-card fade-in delay-5" style="margin-bottom:24px;">
      <div class="form-section-title">
        <svg width="16" height="16" fill="none" stroke="#2d5be3" stroke-width="2" viewBox="0 0 24 24" style="display:inline;margin-right:8px;vertical-align:middle;"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/></svg>
        Contrat & Fournisseur
      </div>
      <div class="form-grid">
        {% for field in form.contrat %}
        <div class="form-group">
          <label for="{{ field.id_for_label }}">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div class="field-error">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
    </div>

    <!-- Section : Développement -->
    <div class="form-card fade-in delay-6" style="margin-bottom:24px;">
      <div class="form-section-title">
        <svg width="16" height="16" fill="none" stroke="#2d5be3" stroke-width="2" viewBox="0 0 24 24" style="display:inline;margin-right:8px;vertical-align:middle;"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
        Développement
      </div>
      <div class="form-grid">
        {% for field in form.developpement %}
        <div class="form-group">
          <label for="{{ field.id_for_label }}">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div class="field-error">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
    </div>

    <!-- Section : Accès & Utilisateurs -->
    <div class="form-card fade-in delay-7" style="margin-bottom:24px;">
      <div class="form-section-title">
        <svg width="16" height="16" fill="none" stroke="#2d5be3" stroke-width="2" viewBox="0 0 24 24" style="display:inline;margin-right:8px;vertical-align:middle;"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
        Accès & Utilisateurs
      </div>
      <div class="form-grid">
        {% for field in form.acces %}
        <div class="form-group">
          <label for="{{ field.id_for_label }}">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div class="field-error">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
    </div>

    <!-- Section : Intégration -->
    <div class="form-card fade-in delay-8" style="margin-bottom:24px;">
      <div class="form-section-title">
        <svg width="16" height="16" fill="none" stroke="#2d5be3" stroke-width="2" viewBox="0 0 24 24" style="display:inline;margin-right:8px;vertical-align:middle;"><path d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
        Intégration
      </div>
      <div class="form-grid">
        {% for field in form.integration %}
        <div class="form-group">
          <label for="{{ field.id_for_label }}">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<div class="field-error">{{ field.errors.0 }}</div>{% endif %}
        </div>
        {% endfor %}
      </div>
    </div>
"""

content = content.replace("<!-- Actions -->", new_sections + "\n    <!-- Actions -->")

# Add some global styles for the generic form inputs generated by django
extra_css = """
  /* Auto-styled generic inputs */
  .form-group input, .form-group select, .form-group textarea {
    width: 100%;
    padding: 10px 14px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 0.85rem;
    font-family: inherit;
    color: #4a5568;
    transition: all 0.2s;
  }
  .form-group input[type="checkbox"] {
    width: auto;
    margin-right: 8px;
  }
"""
content = content.replace("{% endblock %}", extra_css + "\n{% endblock %}", 1)

with open(form_path, "w", encoding="utf-8") as f:
    f.write(content)

update_path = r"c:\Users\ASUS\Icosnet_Traceability_Platform\backend\templates\application_sheet\fiche_update.html"
with open(update_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Forms patched successfully.")
