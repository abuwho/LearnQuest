import React, { useMemo, useState } from "react";
import { Document as MyDocument, Page as MyPage } from "react-pdf";

import 'react-pdf/dist/esm/Page/TextLayer.css';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';


import "./PdfRenderer.css";
import Spinner from "../Spinner";

import { pdfjs } from "react-pdf";

interface Props {
	pdfFile?: string;
}

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
	'pdfjs-dist/build/pdf.worker.min.js',
	import.meta.url,
  ).toString();

const PdfViewer = ({ pdfFile }: Props) => {
	console.log({pdfFile})
	const file = useMemo(() => {
		if (!pdfFile) return null;
		return `http://localhost:8080/${pdfFile}`
		// const blob = new Blob([pdfFile], {
		// 	type: "application/pdf",
		// });
		// return URL.createObjectURL(blob);
	}, [pdfFile]);
	const [numPages, setNumPages] = useState<number>(0);
	const [pageNumber, setPageNumber] = useState(1);

	function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
		console.log({ numPages })
		setNumPages(numPages);
	}

	function changePage(offset: number) {
		setPageNumber((prevPageNumber) => prevPageNumber + offset);
	}

	function previousPage() {
		changePage(-1);
	}

	function nextPage() {
		changePage(1);
	}

	if (typeof window === "undefined") return <Spinner />

	return (
		<div className="pdfContainer">
			{pdfFile && (
				<MyDocument file={file} onLoadSuccess={onDocumentLoadSuccess}>
					<MyPage pageNumber={pageNumber} />
				</MyDocument>
			)}
			<div className="pageNavigation">
				<button onClick={previousPage} disabled={pageNumber <= 1}>
					Previous
				</button>
				<span>
					Page {pageNumber} of {numPages}
				</span>
				<button onClick={nextPage} disabled={pageNumber >= numPages}>
					Next
				</button>
			</div>
		</div>
	);
};

export default PdfViewer;
