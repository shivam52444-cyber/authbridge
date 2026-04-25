def hr_dashboard():
    import streamlit as st
    from databasesetup import SessionLocal
    from schema import Job, Candidate
    from jd_analysis_chain import analyze_jd
    from resume_scoringchain import score_resume
    from resumeparser import extract_text
    from parser import parse_llm_output
    from typing import Optional
    from datetime import datetime
    import re

    st.sidebar.title("HR Panel")

    menu = st.sidebar.radio("Menu", [
        "Active Jobs",
        "Post JD",
        "Pipeline"
    ])

    db = SessionLocal()

    try:
        # =========================
        # ACTIVE JOBS
        # =========================
        if menu == "Active Jobs":
            st.header("Active Job Openings")

            jobs = db.query(Job).all()

            if not jobs:
                st.info("No jobs posted yet")
            else:
                for job in jobs:
                    st.subheader(job.title)
                    st.write(f"📍 {job.location}")
                    st.write(f"🏢 {job.department}")
                    st.write(f"👤 Manager ID: {job.reporting_to}")
                    st.write(f"🕒 {job.posted_at}")
                    st.write(f"🆔 Job ID: {job.jobid}")
                    st.markdown("---")

        # =========================
        # POST JD
        # =========================
        elif menu == "Post JD":
            st.header("Create Job")

            title = st.text_input("Job Title")

            department = st.selectbox(
                "Department",
                ["Engineering", "Product", "Analytics", "HR"]
            )

            location = st.selectbox(
                "Location",
                ["Remote", "Bangalore", "Mumbai", "Delhi"]
            )

            reporting_to = st.number_input("Manager ID", min_value=1)

            jd = st.text_area("Job Description")

            if st.button("Analyze JD"):
                if not jd.strip():
                    st.warning("Enter JD")
                else:
                    result = analyze_jd(jd)

                    count = len(re.findall(r'\n|-', jd))

                    if count > 12:
                        quality = "🔴 Too Hard"
                    elif count < 4:
                        quality = "🟡 Too Soft"
                    elif 6 <= count <= 10:
                        quality = "🟢 Optimal"
                    else:
                        quality = "🟠 Moderate"

                    st.info(f"JD Quality: {quality}")
                    st.write(f"Requirements: {count}")
                    st.text_area("AI Output", result, height=200)

            if st.button("Save Job"):
                if not title or not jd:
                    st.error("Fill all fields")
                else:
                    job = Job(
                        title=title,
                        description=jd,
                        department=department,
                        location=location,
                        reporting_to=int(reporting_to),
                        posted_at=datetime.utcnow()
                    )

                    db.add(job)
                    db.commit()
                    db.refresh(job)

                    st.success(f"Job Created | ID: {job.jobid}")

        # =========================
        # PIPELINE
        # =========================
        elif menu == "Pipeline":
            st.header("Resume Pipeline")

            jobs = db.query(Job).all()

            if not jobs:
                st.warning("No jobs available")
                return

            # Select Job
            job_map = {
                f"{j.title} (ID:{j.jobid})": j.jobid for j in jobs
            }

            selected = st.selectbox("Select Job", list(job_map.keys()))
            job_id = job_map[selected]

            job: Optional[Job] = db.get(Job, job_id)

            if job is None:
                st.error("Invalid Job selected")
                return

            st.subheader("Selected Job Description")
            st.text_area("JD", job.description, height=150)

            # Upload resumes
            files = st.file_uploader(
                "Upload Resumes",
                accept_multiple_files=True,
                type=["pdf"]
            )

            if st.button("Process Resumes"):

                if not files:
                    st.warning("Upload resumes first")
                    return

                progress = st.progress(0)

                for i, file in enumerate(files):
                    try:
                        text = extract_text(file)

                        if not text.strip():
                            st.warning(f"{file.name} skipped")
                            continue

                        ai_output = score_resume(job.description, text)
                        score, parsed = parse_llm_output(ai_output)

                        candidate = Candidate(
                            name=file.name,
                            email="unknown",
                            resume_text=text,
                            job_id=job_id,
                            score=score,
                            summary=str(parsed),
                            status="pending",
                            hr_reason=None,
                            hr_id=None
                        )

                        db.add(candidate)

                    except Exception as e:
                        st.error(f"{file.name}: {e}")

                    progress.progress((i + 1) / len(files))

                db.commit()
                st.success("Resumes processed successfully")

            # =========================
            # CANDIDATE REVIEW
            # =========================
            st.header("Candidate Review")

            candidates = (
                db.query(Candidate)
                .filter_by(job_id=job_id)
                .order_by(Candidate.score.desc())
                .all()
            )

            if not candidates:
                st.info("No candidates yet")

            for c in candidates:
                st.subheader(c.name)

                st.metric("AI Score", f"{c.score:.1f}/100")

                if c.score >= 80:
                    st.success("🔥 Strong Match")
                elif c.score >= 60:
                    st.warning("⚠️ Moderate Match")
                else:
                    st.error("❌ Weak Match")

                st.write(f"Status: {c.status}")

                with st.expander("AI Summary"):
                    st.write(c.summary)

                # Already reviewed
                if c.status != "pending":
                    st.info(f"{c.status.upper()} | Reason: {c.hr_reason}")
                    continue

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Shortlist {c.id}"):
                        st.session_state[f"action_{c.id}"] = "shortlist"

                with col2:
                    if st.button(f"Reject {c.id}"):
                        st.session_state[f"action_{c.id}"] = "reject"

                action = st.session_state.get(f"action_{c.id}")

                if action:
                    reason = st.text_input(
                        "Enter reason",
                        key=f"reason_{c.id}"
                    )

                    if st.button(f"Confirm {c.id}"):

                        if not reason.strip():
                            st.error("Reason required")
                        else:
                            c.status = action
                            c.hr_reason = reason

                            # 🔥 CRITICAL LINE (for leader dashboard)
                            c.hr_id = st.session_state["user_id"]

                            db.commit()
                            st.success(f"{c.name} {c.status}")
                            st.rerun()

    finally:
        db.close()