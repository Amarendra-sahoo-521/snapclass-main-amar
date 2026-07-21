import streamlit as st
import textwrap

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
<div style="margin-bottom:10px;  background-color: transparent; font-family:'Segoe UI', Arial, sans-serif;">
  <div style="width:100%; background:#ffffff; border-radius:16px; padding:20px; box-shadow:0 4px 14px rgba(0,0,0,0.08); border:1px solid #eaeaea;">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
      <h2 style="margin:0; font-size:19px; color:#1f2937; font-weight:700; line-height:1.3;">{name}</h2>
      <span style="background:#eef2ff; color:#4338ca; font-size:12px; font-weight:600; padding:4px 10px; border-radius:20px; white-space:nowrap;">{code}</span>
    </div>
    <p style="margin:0 0 16px 0; font-size:13px; color:#6b7280;">Section {section}</p>
    <div style="height:1px; background:#f0f0f0; margin-bottom:16px;"></div>
"""

    if stats:
        html += '<div style="display:flex; gap:12px;">'
        for icon, label, value in stats:
            html += f'''
<div style="flex:1; display:flex; align-items:center; gap:10px; background:#f9fafb; border-radius:10px; padding:10px 12px;">
  <span style="font-size:20px;">{icon}</span>
  <div>
    <div style="font-size:15px; font-weight:700; color:#1f2937; line-height:1.2;">{value}</div>
    <div style="font-size:11px; color:#9ca3af;">{label}</div>
  </div>
</div>'''
        html += "</div>"

    html += """
  </div>
</div>
"""

    st.markdown(html, unsafe_allow_html=True)
    # col2, col2 = st.columns(2)
    # with col2:
    if footer_callback:
        footer_callback()