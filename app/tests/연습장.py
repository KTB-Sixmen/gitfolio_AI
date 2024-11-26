# 이력서 생성 수정 api
@router.put("/api/resumes/:resumeId", response_model=ResumeResponse)
async def update_resume(resume_id: str, request: ResumeRequest):
    logging.basicConfig(level=logging.INFO)

    # 1. 기존 이력서 데이터 불러오기
    existing_resume = get_resume_from_db(resume_id)
    if not existing_resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # 2. 전체 데이터를 새로운 요청 데이터로 대체
    updated_resume_data = request.dict()  # 요청을 dict로 변환하여 전체 덮어쓰기
    save_resume_to_db(resume_id, updated_resume_data)

    # 3. 응답 반환
    return {
        "time": "2024-10-17T16:59:59.775325",
        "status": "OK",
        "code": "200 OK",
        "message": "요청에 성공했습니다.",
        "result": "이력서 수정이 완료되었습니다."
    }
