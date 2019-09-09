(def nil (list))

; TODO is this necessary?
; Note: Making the rest of the keywords into functions is necessary to make
; them usable in quoted and then evaled code. But this requires implementing
; variadic arguments.
(def eval (lambda (x) (eval x)))
(def quote (lambda (x) (quote x)))
(def if (lambda (pred then else) (if pred then else)))
(def lambda (lambda (args body) (lambda args body)))  ; whoaa

(def filter
	 (lambda (f l)
	   (if (= l nil)
		 nil
		 (if (f (car l))
		   (cons (car l) (filter f (cdr l)))
		   (filter f (cdr l))))))

(def map
	 (lambda (f l)
	   (if (= l nil)
		 nil
		 (cons (f (car l)) (map f (cdr l))))))

(def reduce
	 (lambda (f l init)
	   (if (= l nil)
		 init
		 (reduce f (cdr l) (f init (car l))))))
