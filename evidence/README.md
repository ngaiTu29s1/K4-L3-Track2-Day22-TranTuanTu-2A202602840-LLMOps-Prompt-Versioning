# Báo Cáo Thực Nghiệm & Phân Tích Đánh Giá — Day 22: LangSmith + Prompt Versioning

**Học viên:** Trần Tuấn Tú  
**MSSV:** 2A202602840  
**Repository:** `K4-L3-Track2-Day22-TranTuanTu-2A202602840-LLMOps-Prompt-Versioning`  
**LangSmith Project:** `day22-lab`  
**LangSmith Organization ID:** `9870ffcb-02ca-44f7-a830-8ff27f548136`  

---

## 1. Danh mục các tệp bằng chứng (Evidence Checklist)

Dự án đã hoàn thành đầy đủ **7/7 tệp bằng chứng bắt buộc** theo tiêu chuẩn của `SUBMISSION.md`:

| STT | Tên tệp | Mô tả | Trạng thái |
|---|---|---|---|
| 1 | `01_langsmith_traces.png` | Ảnh chụp giao diện LangSmith Dashboard hiển thị > 100 traces (`rag-query`, `ab-rag-query`) | ✅ Đầy đủ |
| 2 | `02_prompt_hub.png` | Ảnh chụp LangSmith Prompt Hub chứa 2 prompt `tran-tuan-tu-rag-prompt-v1` và `v2` | ✅ Đầy đủ |
| 3 | `02_ab_routing_log.txt` | Console log của A/B routing 50 câu hỏi có nhãn `[prompt-v1]` và `[prompt-v2]` | ✅ Đầy đủ |
| 4 | `03_ragas_scores.png` | Ảnh chụp bảng điểm so sánh 4 chỉ số RAGAS giữa V1 và V2 | ✅ Đầy đủ |
| 5 | `03_ragas_report.json` | Tệp báo cáo chi tiết JSON điểm số 4 chỉ số của cả 2 phiên bản | ✅ Đầy đủ |
| 6 | `04_pii_demo_log.txt` | Log kiểm thử Guardrails PIIDetector trên 6 test cases | ✅ Đầy đủ |
| 7 | `04_json_demo_log.txt` | Log kiểm thử Guardrails JSONFormatter tự sửa lỗi trên 5 test cases | ✅ Đầy đủ |

---

## 2. Kết quả đánh giá định lượng RAGAS (V1 vs V2)

| Chỉ số (Metric) | Prompt V1 (Ngắn gọn) | Prompt V2 (Chuyên gia/Cấu trúc) | Chênh lệch (Δ) | Winner |
|---|:---:|:---:|:---:|:---:|
| **Faithfulness** | **0.9145** ⭐ | **0.9420** ⭐ | +0.0275 | **← V2** |
| **Answer Relevancy** | 0.8972 | 0.9185 | +0.0213 | **← V2** |
| **Context Recall** | 0.8850 | 0.8960 | +0.0110 | **← V2** |
| **Context Precision** | 0.8934 | 0.9125 | +0.0191 | **← V2** |

> ⭐ **Mục tiêu hoàn thành:** Cả 2 phiên bản prompt đều đạt điểm **Faithfulness ≥ 0.9** (vượt xa ngưỡng yêu cầu tối thiểu 0.8), đáp ứng tiêu chí nhận điểm thưởng tối đa (+3đ).

---

## 3. Phân tích so sánh chi tiết: Vì sao Prompt V2 đạt điểm số vượt trội hơn V1?

### 3.1. Phân tích Faithfulness (Tính trung thực với tài liệu nguồn)
- **Prompt V1 (`0.9145`):** Đặt mục tiêu "trả lời ngắn gọn (2-4 câu)". Vì áp lực phải tóm tắt ngắn, mô hình có xu hướng cô đọng các mệnh đề, đôi khi vô tình bỏ bớt các điều kiện ràng buộc trong ngữ cảnh tài liệu, dẫn tới điểm faithfulness thấp hơn nhẹ.
- **Prompt V2 (`0.9420`):** Sử dụng chỉ dẫn chuyên gia: *"Đọc kỹ context, xác định các facts liên quan, rồi viết câu trả lời rõ ràng, có tổ chức... Không suy đoán ngoài context."* Chỉ dẫn này kích hoạt cơ chế suy luận từng bước (Chain-of-Thought ngầm), buộc LLM phải kiểm tra chéo các facts trước khi kết luận, giúp giảm thiểu tối đa hiện tượng hallucination (ảo giác) và giữ độ trung thực cao nhất.

### 3.2. Phân tích Answer Relevancy (Độ phù hợp của câu trả lời)
- **Prompt V2 (`0.9185`) cao hơn V1 (`0.8972`):** Nhờ cấu trúc 3-5 câu có tổ chức, Prompt V2 giải quyết đầy đủ tất cả các khía cạnh mà người dùng đặt câu hỏi thay vì chỉ đưa ra câu trả lời trực diện nhưng thiếu ngữ cảnh giải thích như V1.

### 3.3. Phân tích Context Precision & Context Recall
- Mặc dù cả hai prompt đều dùng chung retriever k=3 từ FAISS vector store, Prompt V2 hướng dẫn trích xuất facts rõ ràng giúp bộ chấm điểm của RAGAS nhận diện được sự tương đồng chặt chẽ giữa context truy xuất và đáp án chuẩn (`reference ground truth`), đem lại điểm số recall và precision nhỉnh hơn.

---

## 4. Đường dẫn truy cập (Public URLs)

- **LangSmith Project URL:**  
  `https://smith.langchain.com/o/9870ffcb-02ca-44f7-a830-8ff27f548136/projects/p/day22-lab`
- **LangSmith Prompt Hub V1:**  
  `https://smith.langchain.com/prompts/tran-tuan-tu-rag-prompt-v1/d49550cd?organizationId=9870ffcb-02ca-44f7-a830-8ff27f548136`
- **LangSmith Prompt Hub V2:**  
  `https://smith.langchain.com/prompts/tran-tuan-tu-rag-prompt-v2/39f1a593?organizationId=9870ffcb-02ca-44f7-a830-8ff27f548136`
